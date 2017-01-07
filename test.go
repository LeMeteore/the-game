package main

import "testing" // The stdlib is good enough

func compare(t *testing.T, desc string, actual string, expected string) {
	t.Logf(desc)
	if actual == expected {
		t.Logf("✓ ") // UTF-8 FTW!
	} else {
		t.Errorf("❌actual: '%s', expected: '%s'", actual, expected)
	}
}

func TestFormat(t *testing.T) {
	d1 := make(map[string]string)
	actual := Format("", d1)
	expected := ""
	compare(t, "empty", actual, expected)

	d2 := make(map[string]string)
	d2["foo"] = "bar"
	actual = Format("@foo@", d2)
	expected =  "bar"
	compare(t, "just one element", actual, expected)

	d3 := make(map[string]string)
	d3["foo"] = "spam"
	d3["bar"] = "eggs"
	actual = Format("@foo@ and @bar@", d3)
	expected = "spam and eggs"
	compare(t, "two elements", actual, expected)

	/*
	 Not sure this is useful. We'll see clear '@'
	 in the generated HTML, which is always a bad
	 sign (clair-text e-mails ...)

	 We could also return out, err but that's painful

	d4 := make(map[string]string)
	d4["foo"] = "spam"
	actual = Format("@bar@", d4)
	expected = "ERROR: @bar@ was not found in dict"
	compare(t, "missing value", actual, expected)

	*/
}
