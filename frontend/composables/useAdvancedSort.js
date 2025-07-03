export const useAdvancedSort = () => {
  
  /**
   * 优化的快速排序算法 - 三路快排，处理重复元素更高效
   * @param {Array} arr - 要排序的数组
   * @param {Function} compareFn - 比较函数
   * @param {number} left - 左边界
   * @param {number} right - 右边界
   */
  const quickSort3Way = (arr, compareFn, left = 0, right = arr.length - 1) => {
    if (left >= right) return
    
    // 三路快排：处理大量重复元素的场景
    const [lt, gt] = partition3Way(arr, compareFn, left, right)
    
    // 递归排序小于和大于基准的部分
    quickSort3Way(arr, compareFn, left, lt - 1)
    quickSort3Way(arr, compareFn, gt + 1, right)
  }
  
  /**
   * 三路分区 - 将数组分为 <pivot, =pivot, >pivot 三部分
   */
  const partition3Way = (arr, compareFn, left, right) => {
    const pivot = arr[left]
    let lt = left      // arr[left+1...lt] < pivot
    let i = left + 1   // arr[lt+1...i-1] = pivot
    let gt = right + 1 // arr[gt...right] > pivot
    
    while (i < gt) {
      const cmp = compareFn(arr[i], pivot)
      if (cmp < 0) {
        swap(arr, lt + 1, i)
        lt++
        i++
      } else if (cmp > 0) {
        swap(arr, i, gt - 1)
        gt--
      } else {
        i++
      }
    }
    swap(arr, left, lt)
    
    return [lt, gt]
  }
  
  /**
   * 混合排序算法 - 小数组用插入排序，大数组用快排
   * @param {Array} data - 原始数据
   * @param {string} field - 排序字段
   * @param {string} direction - 排序方向 'asc' | 'desc'
   */
  const hybridSort = (data, field, direction = 'asc') => {
    if (!data || data.length <= 1) return data
    
    const sortedData = [...data] // 避免修改原数组
    const compareFn = createCompareFn(field, direction)
    
    // 小数组使用插入排序（更快）
    if (sortedData.length <= 10) {
      insertionSort(sortedData, compareFn)
    } else {
      // 大数组使用优化的快速排序
      quickSort3Way(sortedData, compareFn)
    }
    
    return sortedData
  }
  
  const insertionSort = (arr, compareFn) => {
    for (let i = 1; i < arr.length; i++) {
      const key = arr[i]
      let j = i - 1
      
      while (j >= 0 && compareFn(arr[j], key) > 0) {
        arr[j + 1] = arr[j]
        j--
      }
      arr[j + 1] = key
    }
  }
  
//创建比较函数
    
  const createCompareFn = (field, direction) => {
    return (a, b) => {
      let valA = a[field]
      let valB = b[field]
      
      // 处理不同数据类型
      if (typeof valA === 'string') valA = valA.toLowerCase()
      if (typeof valB === 'string') valB = valB.toLowerCase()
      
      // 处理日期
      if (field.includes('date')) {
        valA = new Date(valA).getTime()
        valB = new Date(valB).getTime()
      }
      
      // 处理数字
      if (typeof valA === 'string' && !isNaN(valA)) valA = Number(valA)
      if (typeof valB === 'string' && !isNaN(valB)) valB = Number(valB)
      
      let comparison = 0
      if (valA > valB) comparison = 1
      else if (valA < valB) comparison = -1
      
      return direction === 'asc' ? comparison : -comparison
    }
  }
  
  //交换数组元素
  const swap = (arr, i, j) => {
    [arr[i], arr[j]] = [arr[j], arr[i]]
  }
  
  return {
    hybridSort,
    quickSort3Way,
    insertionSort
  }
}

// 搜索算法
export const useAdvancedSearch = () => {
  
  /**
   * 二分搜索 - 用于已排序数据的快速查找
   * @param {Array} sortedArray - 已排序的数组
   * @param {*} target - 目标值
   * @param {Function} keyFn - 提取键值的函数
   */
  const binarySearch = (sortedArray, target, keyFn = (x) => x) => {
    let left = 0
    let right = sortedArray.length - 1
    
    while (left <= right) {
      const mid = Math.floor((left + right) / 2)
      const midValue = keyFn(sortedArray[mid])
      
      if (midValue === target) {
        return mid
      } else if (midValue < target) {
        left = mid + 1
      } else {
        right = mid - 1
      }
    }
    
    return -1 // 未找到
  }
  
  /**
   * KMP字符串搜索算法 - 优化文本搜索性能
   * @param {string} text - 源文本
   * @param {string} pattern - 搜索模式
   */
  const kmpSearch = (text, pattern) => {
    if (!pattern || !text) return []
    
    const lps = computeLPS(pattern)
    const results = []
    let i = 0 // text的索引
    let j = 0 // pattern的索引
    
    while (i < text.length) {
      if (pattern[j] === text[i]) {
        i++
        j++
      }
      
      if (j === pattern.length) {
        results.push(i - j)
        j = lps[j - 1]
      } else if (i < text.length && pattern[j] !== text[i]) {
        if (j !== 0) {
          j = lps[j - 1]
        } else {
          i++
        }
      }
    }
    
    return results
  }
  
  /**
   * 计算LPS数组（最长前缀后缀）
   */
  const computeLPS = (pattern) => {
    const lps = new Array(pattern.length).fill(0)
    let len = 0
    let i = 1
    
    while (i < pattern.length) {
      if (pattern[i] === pattern[len]) {
        len++
        lps[i] = len
        i++
      } else {
        if (len !== 0) {
          len = lps[len - 1]
        } else {
          lps[i] = 0
          i++
        }
      }
    }
    
    return lps
  }
  
  /**
   * 模糊搜索 - 使用编辑距离算法
   * @param {Array} data - 数据数组
   * @param {string} query - 搜索查询
   * @param {Array} fields - 搜索字段
   * @param {number} threshold - 相似度阈值
   */
  const fuzzySearch = (data, query, fields, threshold = 0.6) => {
    if (!query) return data
    
    const queryLower = query.toLowerCase()
    
    return data
      .map(item => {
        let maxSimilarity = 0
        
        fields.forEach(field => {
          const value = String(item[field] || '').toLowerCase()
          const similarity = calculateSimilarity(queryLower, value)
          maxSimilarity = Math.max(maxSimilarity, similarity)
        })
        
        return { item, similarity: maxSimilarity }
      })
      .filter(result => result.similarity >= threshold)
      .sort((a, b) => b.similarity - a.similarity)
      .map(result => result.item)
  }
  
  /**
   * 计算字符串相似度（Jaro-Winkler算法）
   */
  const calculateSimilarity = (s1, s2) => {
    if (s1 === s2) return 1
    if (s1.length === 0 || s2.length === 0) return 0
    
    // 简化的相似度计算
    const longer = s1.length > s2.length ? s1 : s2
    const shorter = s1.length > s2.length ? s2 : s1
    
    if (longer.includes(shorter)) {
      return shorter.length / longer.length
    }
    
    // 计算编辑距离
    const editDistance = levenshteinDistance(s1, s2)
    return 1 - editDistance / Math.max(s1.length, s2.length)
  }
  
  /**
   * 编辑距离算法（Levenshtein Distance）
   */
  const levenshteinDistance = (s1, s2) => {
    const matrix = []
    
    for (let i = 0; i <= s2.length; i++) {
      matrix[i] = [i]
    }
    
    for (let j = 0; j <= s1.length; j++) {
      matrix[0][j] = j
    }
    
    for (let i = 1; i <= s2.length; i++) {
      for (let j = 1; j <= s1.length; j++) {
        if (s2.charAt(i - 1) === s1.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1]
        } else {
          matrix[i][j] = Math.min(
            matrix[i - 1][j - 1] + 1, // 替换
            matrix[i][j - 1] + 1,     // 插入
            matrix[i - 1][j] + 1      // 删除
          )
        }
      }
    }
    
    return matrix[s2.length][s1.length]
  }
  
  return {
    binarySearch,
    kmpSearch,
    fuzzySearch,
    calculateSimilarity
  }
}

/**
 * 数据结构优化 Composable
 */
export const useDataStructures = () => {
  
  /**
   * 哈希表实现 - 用于快速查找
   */
  class HashTable {
    constructor(size = 53) {
      this.keyMap = new Array(size)
    }
    
    _hash(key) {
      let total = 0
      const WEIRD_PRIME = 31
      for (let i = 0; i < Math.min(key.length, 100); i++) {
        const char = key[i]
        const value = char.charCodeAt(0) - 96
        total = (total * WEIRD_PRIME + value) % this.keyMap.length
      }
      return total
    }
    
    set(key, value) {
      const index = this._hash(key)
      if (!this.keyMap[index]) {
        this.keyMap[index] = []
      }
      this.keyMap[index].push([key, value])
      return index
    }
    
    get(key) {
      const index = this._hash(key)
      if (this.keyMap[index]) {
        for (let i = 0; i < this.keyMap[index].length; i++) {
          if (this.keyMap[index][i][0] === key) {
            return this.keyMap[index][i][1]
          }
        }
      }
      return undefined
    }
  }
  
  // Trie树实现 - 用于自动补全和前缀搜索
  class TrieNode {
    constructor() {
      this.children = {}
      this.isEndOfWord = false
      this.data = null
    }
  }
  
  class Trie {
    constructor() {
      this.root = new TrieNode()
    }
    
    insert(word, data = null) {
      let current = this.root
      for (let char of word.toLowerCase()) {
        if (!current.children[char]) {
          current.children[char] = new TrieNode()
        }
        current = current.children[char]
      }
      current.isEndOfWord = true
      current.data = data
    }
    
    search(word) {
      let current = this.root
      for (let char of word.toLowerCase()) {
        if (!current.children[char]) {
          return false
        }
        current = current.children[char]
      }
      return current.isEndOfWord
    }
    
    startsWith(prefix) {
      let current = this.root
      for (let char of prefix.toLowerCase()) {
        if (!current.children[char]) {
          return []
        }
        current = current.children[char]
      }
      
      const results = []
      this._dfs(current, prefix, results)
      return results
    }
    
    _dfs(node, prefix, results) {
      if (node.isEndOfWord) {
        results.push({ word: prefix, data: node.data })
      }
      
      for (let char in node.children) {
        this._dfs(node.children[char], prefix + char, results)
      }
    }
  }
  
  return {
    HashTable,
    Trie,
    TrieNode
  }
} 