// File: kmp.go
// Author: zzl0 (zhuzhaolong0@gmail.com)
//
// The idea we'll use is to look for "borders" of a string, which are substrings
// that are both a prefix and suffix of the string.  For example, the string
// "aabcaa" has "aa" as a border, while the string "abc" just has the empty
// string as a border.  Borders are useful in KMP because they encode
// information about where we might need to pick up the search when a particular
// match attempt fails.  For example, suppose that we want to match ABABC
// against the string ABABABC.  If we start off by trying to match the string,
// we'll find that they overlap like this:
//
//    ABABABC
//    ABABx
//
// That is, the first four characters match, but the fifth does not.  At this
// point, rather than naively restarting the search at the second character (B),
// or even restarting it at the third position (A), we can instead note that we
// can treat the last two characters of the string we matched (AB) as the first
// two characters of the pattern string ABABC if we just treated it instead as
// though we had
//
//    ABABABC
//    ABABx
//      ABABC
//
// If we can somehow remember the fact that we already matched the AB at the
// start of this string, we could just confirm that the three characters after
// it are ABC and be done.  There's no need to confirm that the characters at
// the front match.
//
// In order to make this possible, we'll construct a special data structure
// called the "fail table."  This table stores, for each possible prefix of the
// string to match, the length of the longest border of that prefix.  That way,
// when we find a mismatch, we know where the next possible start location could
// be found.  In particular, once we have a mismatch, if there's any border of
// the prefix of the pattern that we matched so far, then we can treat the end
// of that matching prefix as the start of a prefix of the word that occurs
// later in the target.
//
// The basic idea behind KMP is, given this table, to execute the following:
//
//  - Guess that the string starts at the beginning of the target.
//  - Match as much of the string as possible.
//  - If the whole string matched, we're done.
//  - Otherwise, a mismatch was found. Look up the largest border of the string
//    that was matched so far in the failure table.
//  - Update our guess of the start position to be where that border occurs
//    in the portion matched so far, then repeat this process.

package main

import "fmt"

// We define the function "Extended Longest Proper Boundary" (xLPB) as follows:
//
//    xLPB(string, n, char) = The longest proper boundary of string[0:n] + char
//
// Notice note for any nonzero n, we have that
//
//    LongestProperBoundary(string[0:n]) = xLPB(string, n - 1, string[n - 1])
//
// We have the following element conclusion to compute LPB.
//
//    xLPB(string, n, char) =
//        if n = 0, then 0.
//        let k = xLPB(string, n - 1, string[n - 1])
//        if string[k] == char, return k + 1
//        else, xLPB(string, k, char)
func failTable(pattern string) []int {
    // table[i] = the length of LongestProperBoundary(pattern[0:i])
    table := make([]int, len(pattern) + 1)

    for i := 0; i < len(pattern); i++ {
        j := i
        for {
            if (j == 0) {
                table[i + 1] = 0;
                break;
            }

            if (pattern[i] == pattern[table[j]]) {
                table[i + 1] = table[j] + 1
                break;
            }

            j = table[j]
        }
    }

    return table;
}

func kmpMatch(needle, haystack string) int {
    fail := failTable(needle)

    index := 0
    match := 0

    for index + match < len(haystack) {
        if haystack[index + match] == needle[match] {
            match += 1

            if match == len(needle) {
                return index
            }
        } else {
            if match == 0 {
                index += 1
            } else {
                index += match - fail[match]
                match = fail[match]
            }
        }
    }

    return -1
}

func main() {
    fmt.Println(kmpMatch("0101", "0011001011"))
    fmt.Println(kmpMatch("ABC", "ABABABACCABC"))
}
