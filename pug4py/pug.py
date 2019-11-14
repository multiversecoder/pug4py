"""
Pug4Py is a simple script that allows you to use all the functions of Pug (NodeJs)
in any python framework with the addition that you can also use the
mako syntax (a popular and fast template engine for python).
"""

__author__ = "Adriano Romanazzo"

import os
import ast
import json
import shutil
import tempfile
import subprocess
import mako.template

from copy import copy
from typing import Optional, Any, Callable, Dict, Tuple


class PugJSException(Exception):
    pass


class YarnNotInstalled(Exception):
    pass


class NodeNotInstalled(Exception):
    pass


class TemplateNotFound(Exception):
    pass


class Pug:

    def __init__(self, template_dir: str) -> None:
        """
        Set the template basedir
        Used by the PugJs engine (node) to render includes and other things
        Used by this script to check if the template exists

        Parameters
        ----------
            template_dir: str
                the main directory of templates

        """
        self.template_dir = os.path.abspath(template_dir)
        if not os.path.exists(f"{os.path.abspath(os.path.dirname(__file__))}/node_modules"):
            print(f"I'm configuring your enviroment to use pug js. At the end of this operation in the Pug module you will find the directory node_modules with its dependencies into {os.path.abspath(os.path.dirname(__file__))}")
            subprocess.Popen(["yarn", "--cwd", os.path.abspath(os.path.dirname(__file__)), "add", "pug"]).wait()

    def __check_if_tpl_exists(self, filename: str) -> None:
        """
        Check if the template exists

        Parameters
        ----------
            filename: str
                the path of the template to render

        Raises
        ------
            TemplateNotFound
                if the template does not exists
        """
        template = os.path.join(self.template_dir, filename)

        if not os.path.exists(template):
            err = f"Cannot find the template {template}\n\
            Check that you have set the right directory for the templates \
            or that you have not made a mistake by typing the name of the template."
            raise TemplateNotFound(err)

    def __check_for_node(self) -> None:
        """
        Check if the node intepreter is installed

        Raises
        ------
            NodeNotInstalled
                If node is not installed in this system
            YarnNotInstalled
                If node is not installed in this system
        """
        if not bool(shutil.which("node")):
            raise NodeNotInstalled(
                "To Run this PugJS Bridge You need to install Node on this system")
        if not bool(shutil.which("yarn")):
            raise YarnNotInstalled(
                "To Run this PugJS Bridge You need to install Yarn Package Manager on this system")

    def __prepare_for_mako(self, filename: str, **kwargs) -> Tuple[Dict[str, Callable], Dict[str, Callable]]:
        """
        This methodo looks for if there are python functions or magic comments
        inside the template to render.

        Note
        ----
            The magic comment is: // mako_vars = [var1, var2, ...]
            This magic comment is sensitive to new lines and will be stripped from html after the transfer to
        the node interpreter.

        After opening the file we look for the magic comment at the beginning of the file and if present
        we add the variables declared into mdict, a dictionary that contains the values to be rendered with mako.
        If there is no magic comment, we analyze the presence of functions within kwargs and if there is a function,
        it is also added to mdict.

        In both cases, any element added in mdict is removed from kwargs

        Returns
        -------
            Tuple[Dict[str, Callable],Dict[str, Callable]]
                The first [0] is a dictionary containing the vars for mako,
                the second [1] is a dictionary containing the vars for node,
        """
        mdict = {}
        kwargs2 = copy(kwargs)

        with open(f"{self.template_dir}/{filename}" if not filename.startswith("/tmp/tmp") else filename) as f:

            content = f.read()

            if content.split("\n", 1)[0].replace(" ", "").startswith("//mako_vars"):
                magic_comment = [f"{el.strip(' ')}" for el in content.split("\n", 1)[0].replace("/", "").split("=")[1].replace(" ", "").replace("[", "").replace("]", "").split(",")]
                for val in magic_comment:
                    for k, v in kwargs.items():
                        if k == val:
                            mdict[k] = v
                            del kwargs2[k]
            for k, v in kwargs.items():
                if hasattr(v, "__call__"):
                    mdict[k] = v
                    del kwargs2[k]

            return mdict, kwargs2


    def __create_tmp_tpl(self, content: str) -> str:
        """
        Creates a temporary file containing the template rendered by mako

        Parameters
        ----------
            content: str
                the content rendered by mako
        Returns
        -------
            str
                the name of the temporary file
        """
        _, temp_tpl = tempfile.mkstemp()
        with open(temp_tpl, "w") as tp:
            tp.write(content)
        return temp_tpl

    def __delete_tmp_file(self, filename: str) -> None:
        """
        Deletes the temporary file

        Parameters
        ----------
            filename: str
                the name of the file to delete
        """
        os.remove(filename)

    def __render_with_mako(self, filename: str, **kwargs) -> str:
        """
        Render the file using mako

        Parameters
        ----------
            filename: str
                the name of the file to render using mako
            kwargs

        Returns
        -------
            str
                the content of the rendered file
        """
        with open(f"{self.template_dir}/{filename}") as tpl:
            tpl = mako.template.Template(
                tpl.read(), strict_undefined=True).render(**kwargs)
        return tpl

    def __create_tmp_json(self, args: dict) -> str:
        """
        Creates a temporary file containing the variables to be passed to the node interpreter using
        json

        Parameters
        ----------
            args: dict
                Args to pass [kwargs]
        Returns
        -------
            str
                the name of the temporary file
        """
        _, temp_json = tempfile.mkstemp()
        with open(temp_json, "w") as tj:
            tj.write(json.dumps(args))
        return temp_json

    def render(self, filename: str, **kwargs) -> Optional[str]:

        self.__check_if_tpl_exists(filename)

        self.__check_for_node()

        mkwargs, kwargs = self.__prepare_for_mako(filename, **kwargs)

        # check if mkwargs is not empty
        if mkwargs != {}:
            mako_rendered = self.__render_with_mako(filename, **mkwargs)
            # creates a temp file with the rendered template to pass to node interpreter
            temp_tpl = self.__create_tmp_tpl(mako_rendered)

        # creates a file with kwargs (json)
        temp_json = self.__create_tmp_json(kwargs)

        # return the pug js rendered template
        ret = subprocess.check_output(["node",
                                       f"{os.path.abspath(os.path.dirname(__file__))}/pug_compile.js",
                                       self.template_dir, filename if "temp_tpl" not in locals() else temp_tpl, temp_json], shell=False).decode("utf-8")

        # deletes the temporary json file
        self.__delete_tmp_file(temp_json)
        # delete the temporary template file if exists
        if "temp_tpl" in locals():
            self.__delete_tmp_file(temp_tpl)

        # if node returned an error, raise an exception
        elif ret.startswith("#<PugJS_Error_for_python>:"):
            raise PugJSException(ret.replace("#<PugJS_Error_for_python>:", ""))

        return ret

