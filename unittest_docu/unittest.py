import unittest
from function_test import entry
import Main

class TestMain(unittest.TestCase):

    def testMain(self):
        resEntryInfo = Main.MainMenu().entryInfo('Matheo', 'ali.dinarvand1370@gmail.com', 'Matheo1370', 'Germany')
        self.assertEquals(resEntryInfo,[(1, 'Matheo', 'ali.dinarvand1370@gmail.com', 'Matheo1370', 'Germany')])

    def testChat(self):
        resChat = Main.Chat().message_recv('Hallo world')
        self.assertEqual(resChat, 'Hallo world')


if __name__== '__main__':
    unittest.main()

