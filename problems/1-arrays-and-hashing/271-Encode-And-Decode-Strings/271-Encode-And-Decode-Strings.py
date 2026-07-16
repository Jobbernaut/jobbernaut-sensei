'''
https://leetcode.com/problems/encode-and-decode-strings/description/
'''

last_solved     = "2026-06-15"
revisit_in_days = 90
times_reviewed  = 6
difficulty      = "medium"
topic_tags      = ["arrays", "hashing"]

# Finite State Automaton solution
# State change triggered by "#"
# State 0: Reading mode
# State 1: Writing mode
class Codec:
    def encode(self, strs: List[str]) -> str:
        """Encodes a list of strings to a single string.
        """
        output = []

        for string in strs:
            output.append("{}#{}".format(len(string), string))
        
        return "".join(output)
        

    def decode(self, s: str) -> List[str]:
        """Decodes a single string to a list of strings.
        """
        read_len = ""
        write_str = ""
        state = 0
        output = []
        pointer = 0
        # Start automaton in reading mode
        while pointer < len(s):
            if state == 0:
                if s[pointer].isnumeric():
                    read_len += s[pointer]
                elif s[pointer] == "#":
                    # State transition to writing mode
                    state = 1
                pointer += 1
            if state == 1:
                end_len = pointer + int(read_len)
                while pointer < end_len:
                    write_str += s[pointer]
                    pointer += 1
                output.append(write_str)
                # State transition back to reading mode
                state = 0
                read_len = ""
                write_str = ""
        return output

# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.decode(codec.encode(strs))
