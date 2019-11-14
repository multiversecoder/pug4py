from pug4py.pug import Pug

if __name__ == '__main__':

    pug = Pug("pug")

    def say_hello():
        return "Hello World"

    print(pug.render("example.pug", say_hello=say_hello, year="2019", author="https://github.com/multiversecoder/pug4py"))

