// LeetCode Problems Database
const PROBLEMS = {
  'two-sum': {
    id: 1,
    title: 'Two Sum',
    difficulty: 'Easy',
    tags: ['Array', 'Hash Map'],
    description: `Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.`,
    constraints: [
      '2 <= nums.length <= 10⁴',
      '-10⁹ <= nums[i] <= 10⁹',
      '-10⁹ <= target <= 10⁹',
      'Only one valid answer exists.'
    ],
    examples: [
      {
        input: 'nums = [2,7,11,15], target = 9',
        output: '[0,1]',
        explanation: 'Because nums[0] + nums[1] == 9, we return [0, 1].'
      },
      {
        input: 'nums = [3,2,4], target = 6',
        output: '[1,2]',
        explanation: ''
      },
      {
        input: 'nums = [3,3], target = 6',
        output: '[0,1]',
        explanation: ''
      }
    ],
    starterCode: {
      python: `def two_sum(nums, target):
    # Your code here
    pass

# Test
print(two_sum([2,7,11,15], 9))  # Expected: [0,1]`,
      javascript: `function twoSum(nums, target) {
    // Your code here
}

// Test
console.log(twoSum([2,7,11,15], 9));  // Expected: [0,1]`,
      typescript: `function twoSum(nums: number[], target: number): number[] {
    // Your code here
    return [];
}

// Test
console.log(twoSum([2,7,11,15], 9));  // Expected: [0,1]`
    },
    testCases: [
      { input: '[2,7,11,15]\n9', expected: '[0, 1]' },
      { input: '[3,2,4]\n6', expected: '[1, 2]' },
      { input: '[3,3]\n6', expected: '[0, 1]' }
    ]
  },
  'valid-parentheses': {
    id: 20,
    title: 'Valid Parentheses',
    difficulty: 'Easy',
    tags: ['Stack', 'String'],
    description: `Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
- Open brackets must be closed by the same type of brackets.
- Open brackets must be closed in the correct order.
- Every close bracket has a corresponding open bracket of the same type.`,
    constraints: [
      '1 <= s.length <= 10⁴',
      's consists of parentheses only \'()[]{}\'.'
    ],
    examples: [
      {
        input: 's = "()"',
        output: 'true',
        explanation: ''
      },
      {
        input: 's = "()[]{}"',
        output: 'true',
        explanation: ''
      },
      {
        input: 's = "(]"',
        output: 'false',
        explanation: ''
      }
    ],
    starterCode: {
      python: `def is_valid(s):
    # Your code here
    pass

# Test
print(is_valid("()"))  # Expected: True`,
    },
    testCases: [
      { input: '()', expected: 'True' },
      { input: '()[]{}', expected: 'True' },
      { input: '(]', expected: 'False' }
    ]
  },
  'reverse-linked-list': {
    id: 206,
    title: 'Reverse Linked List',
    difficulty: 'Easy',
    tags: ['Linked List'],
    description: `Given the head of a singly linked list, reverse the list, and return the reversed list.`,
    constraints: [
      'The number of nodes in the list is the range [0, 5000].',
      '-5000 <= Node.val <= 5000'
    ],
    examples: [
      {
        input: 'head = [1,2,3,4,5]',
        output: '[5,4,3,2,1]',
        explanation: ''
      },
      {
        input: 'head = [1,2]',
        output: '[2,1]',
        explanation: ''
      },
      {
        input: 'head = []',
        output: '[]',
        explanation: ''
      }
    ],
    starterCode: {
      python: `# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    # Your code here
    pass`,
    },
    testCases: []
  }
};

export default PROBLEMS;
