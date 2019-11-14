from pug4py.pug import Pug

if __name__ == '__main__':

    pug = Pug("pug")

    greet="Hi Bro"
    print(pug.render("example_includes.pug", year="2019", author="https://github.com/multiversecoder/pug4py"))

