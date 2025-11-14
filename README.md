# Assorted

1. Web + iOS + Android + Backend for a photo album

   1. Create an album
   2. Upload images to the album
   3. Convert images to webp formats:
      1. Normal version: width at most 1920px and height at most 1080px; aspect ratio unchanged.
      2. Thumbnail version: width and height at most 512px, aspect ratio 1:1, scaled and center-cropped vertically and horizontally.
      3. Store the images persistently.
   4. View album's image thumbnails and enlarged version when clicked
   5. Delete a single image in an album
   6. Delete an album

   # Usage

   1. Launch the service

   ```bash
    docker compose up -d
   ```

   2. visit http://localhost:3000

   # Demo

   - [Web demo](https://youtu.be/KgrUGN3wmwY)
   - [Mobile demo](https://youtube.com/shorts/PIWyiIpn-OI?feature=share)

2. LeetCode
   1. https://leetcode.com/problems/find-common-characters/description/
      a: https://leetcode.com/problems/find-common-characters/submissions/1825278714

      ```javascript
      /**
       * @param {string[]} words
       * @return {string[]}
       */
      var commonChars = function (words) {
        let unique_char = [...new Set(words.join("").split(""))];
        let common = unique_char.filter((char) =>
          words.every((word) => word.includes(char))
        );
        const appearance = findCharacterAppeaence(common, words);
        const result = [];
        for (let key in appearance) {
          for (let i = 0; i < appearance[key]; i++) {
            result.push(key);
          }
        }
        return result;
      };

      function findCharacterAppeaence(common, words) {
        const result = {};
        for (let word of words) {
          for (let char of common) {
            let count = 0;
            for (let c of word) {
              if (char === c) count++;
            }
            if (result[char] === undefined) result[char] = Infinity;
            result[char] = Math.min(result[char], count);
          }
        }
        return result;
      }
      ```

   2. https://leetcode.com/problems/count-the-number-of-good-nodes/description/
      a: https://leetcode.com/problems/count-the-number-of-good-nodes/submissions/1826121433/ (DNF)

      ```javascript
      /**
       * @param {number[][]} edges
       * @return {number}
       */

      var countGoodNodes = function (edges) {
        const node_amount = edges.length + 1;
        const max = edges.length - 1;
        let good = 0;
        good += verify(max, edges);
        return good;
      };

      function verify(n, list) {
        if (n === 0) {
          return 1;
        }
        if (list[n - 1][0] === list[n][0]) {
          return verify(n - 1, list);
        }
      }

      // Step to solve:
      // 1. Find shared head
      // 2. Verify all sub node of head have same size
      // 3. If so, it is a good node. Otherwise it is not.

      // Step to solve:
      // 1. Sort the given list to node group (if node member <= 2, the head node is a good node)
      // 2. Verify each group
      ```

   3. https://leetcode.com/problems/first-missing-positive/description/
      a: https://leetcode.com/problems/first-missing-positive/submissions/1827072513 (DNF)

      ```javascript
      /**
       * @param {number[]} nums
       * @return {number}
       */
      Object.defineProperty(Array.prototype, "count", {
        value: function (value) {
          return this.filter((e) => e === value).length;
        },
      });

      var firstMissingPositive = function (nums) {
        const max = Math.max(...nums) + 1;
        const count = Array.from({ length: max }, () => 0);
        const anwser = Array.from({ length: nums.length });

        for (let i = 0; i < nums.length; i++) {
          let n = nums[i];
          count[n] = nums.count(n) > 0 ? nums.count(n) + n : nums.count(n);
          anwser[count[n] - 1] = n;
        }
        for (let i = 0; i < nums.length; i++) {
          if (anwser[i] !== i) return i + 1;
          if (i === nums.length - 1) return i + 1;
        }
      };

      // Step to solve:
      // Sort the array
      // Use indice 0...max(...nums) to find
      ```

# Notes

1. Languages
   1. Programming languages: C/C++/JavaScript/TypeScript/Python3/Go/Swift/Kotlin
   2. Natural languages: English
2. Album
   1. Please provide README.md with instructions to run locally
   2. Docker compose is recommended
3. LeetCode
   1. Only code snippets are required
   2. The snippets must be accepted by LeetCode
4. System
   1. macOS or Linux
5. Quality expectation
   1. Everything can be examined, make sure you tried your best. No need to rush.
6. Getting started
   1. Make a fork of this repository and start coding now!.
