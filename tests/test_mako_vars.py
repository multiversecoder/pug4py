from pug4py.pug import Pug

if __name__ == '__main__':

    pug = Pug("pug")

    def say_hello():
        return "Hello World"

    greet="Hi Bro"
    print(pug.render("example_mako_vars.pug", say_hello=say_hello, greet=greet, year="2019", author="https://github.com/multiversecoder/pug4py"))

