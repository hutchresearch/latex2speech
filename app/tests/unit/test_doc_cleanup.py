import unittest

from doc_cleanup import cleanxml_string

class TestDocCleanup(unittest.TestCase):

    # Find illegal amp &
    def test_illegal_amp(self):
        doc = r"&"
        self.assertEqual(cleanxml_string(doc), "&amp;")

        doc = r"& "
        self.assertEqual(cleanxml_string(doc), "&amp; ")

        doc = r" & "
        self.assertEqual(cleanxml_string(doc), " &amp; ")

        doc = r"&words Testing"
        self.assertEqual(cleanxml_string(doc), "&amp;words Testing")
        
    # Find illegal < that appear before <
    def test_illegal_lt(self):
        doc = r"<"
        self.assertEqual(cleanxml_string(doc), "&lt;")

        doc = r"<test>"
        self.assertEqual(cleanxml_string(doc), "<test>")

        doc = r"<>"
        self.assertEqual(cleanxml_string(doc), "<>")

        doc = r"<a word is there< < you know? <"
        self.assertEqual(cleanxml_string(doc), "&lt;a word is there&lt; &lt; you know? &lt;")

    # Find illegal <<<< trail
    def test_illegal_lt_trail(self):
        doc = r"<<"
        self.assertEqual(cleanxml_string(doc), "&lt;&lt;")

        doc = r"<test>"
        self.assertEqual(cleanxml_string(doc), "<test>")

        doc = r"<>"
        self.assertEqual(cleanxml_string(doc), "<>")

        doc = r"<<<<<<Just a word> Hey guys! <<"
        self.assertEqual(cleanxml_string(doc), "&lt;&lt;&lt;&lt;&lt;<Just a word> Hey guys! &lt;&lt;")
        
    # Find illegal > trail
    def test_illegal_gt(self):
        doc = r">"
        self.assertEqual(cleanxml_string(doc), "&gt;")

        doc = r"<test>"
        self.assertEqual(cleanxml_string(doc), "<test>")

        doc = r"<>"
        self.assertEqual(cleanxml_string(doc), "<>")

        doc = r">a word is there> > you know? >"
        self.assertEqual(cleanxml_string(doc), "&gt;a word is there&gt; &gt; you know? &gt;")

    # Find illegal >>>>
    def test_illegal_gt_trail(self):
        doc = r">>"
        self.assertEqual(cleanxml_string(doc), "&gt;&gt;")

        doc = r"<test>"
        self.assertEqual(cleanxml_string(doc), "<test>")

        doc = r"<>"
        self.assertEqual(cleanxml_string(doc), "<>")

        doc = r">>>>>>Just a word> Hey guys! >>"
        self.assertEqual(cleanxml_string(doc), "&gt;&gt;&gt;&gt;&gt;&gt;Just a word&gt; Hey guys! &gt;&gt;")