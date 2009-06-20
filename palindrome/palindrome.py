#!/usr/bin/python
import doctest

"""This program finds the longest palindrome in a given string.

The algorithm works as follows:
    Assume for simplicity that the palindrome is a length that is an odd
    number. Also, we treat a single character as a palindrome of length 1. 

    For each position in the string we store an upper and lower pointer
    that tracks the upper and lower bounds of the largest palindrome centered
    at that position.

    For instance, position 2 in the string "racecar" would start as:

    i.e.      lower
                |
               \|/
            r a c e c a r
               /|\ 
                |
              upper  

    At this point, the longest known palindrome at position 2 is the single
    character 'c'. We then increment the upper pointer and decrement the lower
    pointer and compare their respective values.

    i.e.    lower
              |
             \|/
            r a c e c a r
                 /|\ 
                  |
                upper  

    Since the upper and lower values are not the same, we stop and now know
    that the longest palindrome centered at position 2 is 'c'. We then start
    the process again at the next string position, 3.
    
    i.e.        lower
                  |
                 \|/
            r a c e c a r
                 /|\ 
                  |
                upper  

    We increment and decrement the upper and lower pointers and see that they
    are equal. Our current longest palindrome centered at position 3 is now
    'cec'.

    i.e.      lower
                |
               \|/
            r a c e c a r
                   /|\ 
                    |
                  upper 

    Since they were equal, we increment and decrement the pointers again and
    see that they are still equal. Our new longest palindrome centered at
    position 3 is now 'acece'.

    i.e.    lower
              |
             \|/
            r a c e c a r
                     /|\ 
                      |
                    upper 

    We continue incrementing and decrementing the upper and lower pointers
    until they don't match or they hit one of the ends of the string.
    
    Since our pointers are equal, we increment and decrement them again.
    We hit an end of the string and the pointers are equal so we know that
    our longest palindrome centered at position 3 is 'racecar'.

    i.e.  lower
            |
           \|/
            r a c e c a r
                       /|\ 
                        |
                      upper 

    We're done with position 3 and continue this same process again at
    position 4. We'll do this until we've covered every position in the string.

    NOTE: We initally assumed that the palindrome had an odd length. This
    algorithm works for even palindromes as well. The only change we make is
    that when we initialize the pointers, instead of having the lower and upper
    pointer point to the same position we have the upper pointer point at the
    next position. Everything else with the algorithm remains the same.

    i.e. The initial pointers for an even palindrome 'centered' at position 3
    would look like:
                lower
                  |
                 \|/
            r a c e c a r
                   /|\ 
                    |
                  upper 

The algorithm's runtime is:
    Worst-Case: O(N^2)
    Best-Case:  O(N)

The worst case is achieved when the string is a single repeated character
because every substring is a palindrome.

The best case is achieved when the string contains no palindromes.

Typically if a string only contains a single palindrome (the fewer the
better), the closer to O(N) it will run. This is because everytime it checks
a position in the string, it checks the character before and after that
position, and if they don't match then it stops looking for the palindrome.
Positions in the string can be discarded after only one lookup if that position
doesn't have a palindrome, so if there are no palindromes you only do N
comparisons.
"""

def findLongestPalindrome(string):
    """Given a string, returns the longest palindrome within that string.
    
    -- Doctests --
    
    Empty string
    >>> findLongestPalindrome('')
    ''

    Single character
    >>> findLongestPalindrome('a')
    'a'

    Double character string, odd length palindrome
    >>> findLongestPalindrome('ab')
    'a'

    Double character string, even length palindrome
    >>> findLongestPalindrome('aa')
    'aa'

    Triple character string, double character palindrome at start
    >>> findLongestPalindrome('bba')
    'bb'

    Triple character string, double character palindrome at end
    >>> findLongestPalindrome('abb')
    'bb'

    Triple character string, triple character palindrome
    >>> findLongestPalindrome('aba')
    'aba'

    Single odd palindrome in sentence.
    >>> findLongestPalindrome('Very fast racecar.')
    'racecar'

    Single even palindrome in sentence.
    >>> findLongestPalindrome('James Joyce said tattarrattat in Ulysses') 
    ' tattarrattat '

    Several palindromes of varying length, confirm longest is chosen
    >>> findLongestPalindrome('a bb aba abba abcba cddc cdc dd c')
    'ba abba ab'

    """
    # Initially, our longest known palindrome is the empty string
    longest = ""

    # We find the longest palindrome centered at each position and return the
    # longest one we find
    for position in xrange(len(string)):
        longest = max(longest, getPalindromeAt(position, string), key = lambda a: len(a))
    return longest

def getPalindromeAt(position, string):
    """Given a position in a string, and the string, this will return the
    longest palindrome centered at that position.

    -- Doctests --

    Empty string
    >>> getPalindromeAt(0, '')
    ''

    Single character
    >>> getPalindromeAt(0, 'a')
    'a'

    Double character, first position
        Single character palindrome
        >>> getPalindromeAt(0, 'ab')
        'a'

        Double character palindrome
        >>> getPalindromeAt(0, 'aa')
        'aa'

    Double character, second position
        Single palindrome
        >>> getPalindromeAt(1, 'aa')
        'a'

    Triple character, first position
        Single palindrome
        >>> getPalindromeAt(0, 'abc')
        'a'

        Double palindrome
        >>> getPalindromeAt(0, 'aab')
        'aa'

    Triple character, second position
        Single palindrome
        >>> getPalindromeAt(1, 'abc')
        'b'

        Double palindrome
        >>> getPalindromeAt(1, 'abb')
        'bb'

        Triple palindrome
        >>> getPalindromeAt(1, 'aba')
        'aba'

    Triple character, third position
        Single palindrome
        >>> getPalindromeAt(2, 'abc')
        'c'

    Check position after end of string
    >>> getPalindromeAt(7, 'racecar')
    ''

    Check position before start of string
    >>> getPalindromeAt(-1, 'racecar')
    ''

    """
    # Initially,the longest known palindrome is the character at this position
    longest = (position, position)

    # For an odd palindrome, we initiate the lower and upper pointers to the
    # current position plus/minus one. For an even palindrome we only add
    # one to the upper pointer.
    for lower, upper in [(position - 1, position + 1), (position, position + 1)]:

        # We keep incrementing and decrementing the pointers until they are no
        # longer equal, or an end of the string is hit
        while lower >= 0 and upper < len(string) and string[lower] == string[upper]:
            upper += 1
            lower -= 1
        longest = max(longest, (lower + 1, upper - 1), key = lambda a: a[1] - a[0])
    return string[longest[0] : longest[1] + 1]

if __name__ == "__main__":
    # Run the doctests for this module
    import doctest
    doctest.testmod()
