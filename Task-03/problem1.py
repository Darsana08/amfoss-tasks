Palindrome number
Given an integer x, return true if x is a palindrome, and false otherwise.

class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        
        # Negative numbers and numbers ending in 0 (except 0 itself) cannot be palindromes
        if x < 0 or (x % 10 == 0 and x != 0):
            return False
        
        reverted_number = 0
        while x > reverted_number:
            reverted_number = reverted_number * 10 + x % 10
            x //= 10
            
        # When the length is an odd number, we can get rid of the middle digit by reverted_number // 10
        return x == reverted_number or x == reverted_number // 10
