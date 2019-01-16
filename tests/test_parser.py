from app.utils.parser import Parser

class TestParser:
    def setup(self):
        print('setup')
        text = "parser  text, éééé --_[]{,; 123 le à de d'"
        self.parser = Parser(text)
        self.output = self.parser.parse()

    def test_parser(self):
        assert self.output == 'parser text eeee 123'
