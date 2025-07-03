/**
 * 动态规划算法 Composable - 用于薪资优化和资源分配
 * 应用背包问题、最优子结构等经典DP算法
 */

export const useDynamicProgramming = () => {
  
  /**
   * 0-1背包问题 - 优化薪资预算分配
   * @param {Array} employees - 员工数组 [{id, name, salary, value, department}]
   * @param {number} budget - 总预算
   */
  const knapsackSalaryOptimization = (employees, budget) => {
    const n = employees.length
    const dp = Array(n + 1).fill().map(() => Array(budget + 1).fill(0))
    const keep = Array(n + 1).fill().map(() => Array(budget + 1).fill(false))
    
    // 动态规划填表
    for (let i = 1; i <= n; i++) {
      const employee = employees[i - 1]
      const salary = Math.floor(employee.salary || 0)
      const value = employee.value || 1 // 员工价值评分
      
      for (let w = 0; w <= budget; w++) {
        if (salary <= w) {
          const includeValue = dp[i - 1][w - salary] + value
          const excludeValue = dp[i - 1][w]
          
          if (includeValue > excludeValue) {
            dp[i][w] = includeValue
            keep[i][w] = true
          } else {
            dp[i][w] = excludeValue
          }
        } else {
          dp[i][w] = dp[i - 1][w]
        }
      }
    }
    
    // 回溯找到最优解
    const selectedEmployees = []
    let w = budget
    for (let i = n; i > 0 && w > 0; i--) {
      if (keep[i][w]) {
        selectedEmployees.push(employees[i - 1])
        w -= Math.floor(employees[i - 1].salary || 0)
      }
    }
    
    return {
      maxValue: dp[n][budget],
      selectedEmployees: selectedEmployees.reverse(),
      totalCost: selectedEmployees.reduce((sum, emp) => sum + (emp.salary || 0), 0),
      efficiency: dp[n][budget] / budget
    }
  }
  
  /**
   * 完全背包问题 - 培训资源分配优化
   * @param {Array} trainingPrograms - 培训项目 [{cost, benefit, capacity}]
   * @param {number} budget - 培训预算
   */
  const trainingResourceOptimization = (trainingPrograms, budget) => {
    const dp = Array(budget + 1).fill(0)
    const choices = Array(budget + 1).fill().map(() => [])
    
    for (let w = 1; w <= budget; w++) {
      for (let i = 0; i < trainingPrograms.length; i++) {
        const program = trainingPrograms[i]
        const cost = Math.floor(program.cost)
        const benefit = program.benefit
        
        if (cost <= w) {
          const newBenefit = dp[w - cost] + benefit
          if (newBenefit > dp[w]) {
            dp[w] = newBenefit
            choices[w] = [...choices[w - cost], program]
          }
        }
      }
    }
    
    return {
      maxBenefit: dp[budget],
      selectedPrograms: choices[budget],
      totalCost: choices[budget].reduce((sum, prog) => sum + prog.cost, 0),
      roi: dp[budget] / budget
    }
  }
  
  /**
   * 最长递增子序列 - 员工职业发展路径优化
   * @param {Array} careerSteps - 职业步骤 [{level, salary, skills, time}]
   */
  const longestIncreasingSubsequence = (careerSteps) => {
    if (!careerSteps.length) return { length: 0, sequence: [] }
    
    const n = careerSteps.length
    const dp = Array(n).fill(1)
    const prev = Array(n).fill(-1)
    
    for (let i = 1; i < n; i++) {
      for (let j = 0; j < i; j++) {
        if (careerSteps[j].level < careerSteps[i].level && 
            careerSteps[j].salary < careerSteps[i].salary) {
          if (dp[j] + 1 > dp[i]) {
            dp[i] = dp[j] + 1
            prev[i] = j
          }
        }
      }
    }
    
    // 找到最长序列的结束位置
    let maxLength = 0
    let lastIndex = 0
    for (let i = 0; i < n; i++) {
      if (dp[i] > maxLength) {
        maxLength = dp[i]
        lastIndex = i
      }
    }
    
    // 重构序列
    const sequence = []
    let current = lastIndex
    while (current !== -1) {
      sequence.unshift(careerSteps[current])
      current = prev[current]
    }
    
    return {
      length: maxLength,
      sequence,
      totalSalaryIncrease: sequence.length > 1 ? 
        sequence[sequence.length - 1].salary - sequence[0].salary : 0
    }
  }
  
  /**
   * 编辑距离 - 员工技能匹配优化
   * @param {Array} requiredSkills - 职位要求的技能
   * @param {Array} employeeSkills - 员工现有技能
   */
  const skillMatchingDistance = (requiredSkills, employeeSkills) => {
    const m = requiredSkills.length
    const n = employeeSkills.length
    const dp = Array(m + 1).fill().map(() => Array(n + 1).fill(0))
    
    // 初始化
    for (let i = 0; i <= m; i++) dp[i][0] = i
    for (let j = 0; j <= n; j++) dp[0][j] = j
    
    // 填充DP表
    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        if (requiredSkills[i - 1] === employeeSkills[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1]
        } else {
          dp[i][j] = 1 + Math.min(
            dp[i - 1][j],     // 删除
            dp[i][j - 1],     // 插入
            dp[i - 1][j - 1]  // 替换
          )
        }
      }
    }
    
    // 计算匹配度
    const maxSkills = Math.max(m, n)
    const matchPercentage = maxSkills > 0 ? 
      ((maxSkills - dp[m][n]) / maxSkills) * 100 : 100
    
    return {
      editDistance: dp[m][n],
      matchPercentage,
      missingSkills: requiredSkills.filter(skill => 
        !employeeSkills.includes(skill)
      ),
      extraSkills: employeeSkills.filter(skill => 
        !requiredSkills.includes(skill)
      )
    }
  }
  
  /**
   * 最大子数组和 - 部门绩效优化
   * @param {Array} departmentPerformance - 部门月度绩效数组
   */
  const maxSubarraySum = (departmentPerformance) => {
    if (!departmentPerformance.length) return { maxSum: 0, start: 0, end: 0 }
    
    let maxSum = departmentPerformance[0]
    let currentSum = departmentPerformance[0]
    let start = 0
    let end = 0
    let tempStart = 0
    
    for (let i = 1; i < departmentPerformance.length; i++) {
      if (currentSum < 0) {
        currentSum = departmentPerformance[i]
        tempStart = i
      } else {
        currentSum += departmentPerformance[i]
      }
      
      if (currentSum > maxSum) {
        maxSum = currentSum
        start = tempStart
        end = i
      }
    }
    
    return {
      maxSum,
      start,
      end,
      bestPeriod: departmentPerformance.slice(start, end + 1),
      averagePerformance: maxSum / (end - start + 1)
    }
  }
  
  /**
   * 硬币找零问题 - 薪资调整组合优化
   * @param {Array} adjustmentOptions - 调薪选项 [100, 200, 500, 1000]
   * @param {number} targetAdjustment - 目标调薪金额
   */
  const salaryAdjustmentCombinations = (adjustmentOptions, targetAdjustment) => {
    const dp = Array(targetAdjustment + 1).fill(Infinity)
    const choice = Array(targetAdjustment + 1).fill(-1)
    dp[0] = 0
    
    for (let amount = 1; amount <= targetAdjustment; amount++) {
      for (let i = 0; i < adjustmentOptions.length; i++) {
        const option = adjustmentOptions[i]
        if (option <= amount && dp[amount - option] + 1 < dp[amount]) {
          dp[amount] = dp[amount - option] + 1
          choice[amount] = option
        }
      }
    }
    
    // 重构解决方案
    const solution = []
    let remaining = targetAdjustment
    while (remaining > 0 && choice[remaining] !== -1) {
      const coin = choice[remaining]
      solution.push(coin)
      remaining -= coin
    }
    
    return {
      minAdjustments: dp[targetAdjustment],
      adjustmentBreakdown: solution,
      isPossible: dp[targetAdjustment] !== Infinity
    }
  }
  
  /**
   * 矩阵链乘法 - 优化报表计算顺序
   * @param {Array} matrices - 矩阵维度数组 [p0, p1, p2, ..., pn]
   */
  const matrixChainMultiplication = (matrices) => {
    const n = matrices.length - 1
    if (n <= 1) return { minCost: 0, order: [] }
    
    const dp = Array(n).fill().map(() => Array(n).fill(0))
    const split = Array(n).fill().map(() => Array(n).fill(0))
    
    // l是链长
    for (let l = 2; l <= n; l++) {
      for (let i = 0; i < n - l + 1; i++) {
        const j = i + l - 1
        dp[i][j] = Infinity
        
        for (let k = i; k < j; k++) {
          const cost = dp[i][k] + dp[k + 1][j] + 
                      matrices[i] * matrices[k + 1] * matrices[j + 1]
          
          if (cost < dp[i][j]) {
            dp[i][j] = cost
            split[i][j] = k
          }
        }
      }
    }
    
    // 构建最优括号化
    const buildOrder = (i, j) => {
      if (i === j) return `M${i}`
      return `(${buildOrder(i, split[i][j])} × ${buildOrder(split[i][j] + 1, j)})`
    }
    
    return {
      minCost: dp[0][n - 1],
      order: n > 1 ? buildOrder(0, n - 1) : 'M0'
    }
  }
  
  return {
    knapsackSalaryOptimization,
    trainingResourceOptimization,
    longestIncreasingSubsequence,
    skillMatchingDistance,
    maxSubarraySum,
    salaryAdjustmentCombinations,
    matrixChainMultiplication
  }
}

/**
 * 高级优化算法 Composable
 */
export const useAdvancedOptimization = () => {
  
  /**
   * 遗传算法 - 员工排班优化
   * @param {Array} employees - 员工数组
   * @param {Array} shifts - 班次要求
   * @param {Object} constraints - 约束条件
   */
  const geneticAlgorithmScheduling = (employees, shifts, constraints) => {
    const populationSize = 50
    const generations = 100
    const mutationRate = 0.1
    const crossoverRate = 0.8
    
    // 生成初始种群
    const generateIndividual = () => {
      const schedule = {}
      shifts.forEach(shift => {
        const availableEmployees = employees.filter(emp => 
          emp.availableShifts?.includes(shift.id)
        )
        schedule[shift.id] = availableEmployees
          .sort(() => Math.random() - 0.5)
          .slice(0, shift.requiredStaff)
      })
      return schedule
    }
    
    // 计算适应度
    const calculateFitness = (individual) => {
      let fitness = 0
      
      // 检查每个班次是否有足够人员
      shifts.forEach(shift => {
        const assigned = individual[shift.id] || []
        if (assigned.length >= shift.requiredStaff) {
          fitness += 10
        } else {
          fitness -= (shift.requiredStaff - assigned.length) * 5
        }
      })
      
      // 检查员工工作时间约束
      const employeeHours = {}
      Object.values(individual).flat().forEach(emp => {
        employeeHours[emp.id] = (employeeHours[emp.id] || 0) + 8
      })
      
      Object.entries(employeeHours).forEach(([empId, hours]) => {
        if (hours <= constraints.maxHoursPerWeek) {
          fitness += 5
        } else {
          fitness -= (hours - constraints.maxHoursPerWeek)
        }
      })
      
      return fitness
    }
    
    // 初始化种群
    let population = Array(populationSize).fill().map(generateIndividual)
    
    // 进化过程
    for (let gen = 0; gen < generations; gen++) {
      // 计算适应度
      const fitnessScores = population.map(calculateFitness)
      
      // 选择
      const newPopulation = []
      for (let i = 0; i < populationSize; i++) {
        // 锦标赛选择
        const tournament = []
        for (let j = 0; j < 3; j++) {
          const randomIndex = Math.floor(Math.random() * population.length)
          tournament.push({
            individual: population[randomIndex],
            fitness: fitnessScores[randomIndex]
          })
        }
        tournament.sort((a, b) => b.fitness - a.fitness)
        newPopulation.push(tournament[0].individual)
      }
      
      population = newPopulation
    }
    
    // 返回最佳解
    const finalFitness = population.map(calculateFitness)
    const bestIndex = finalFitness.indexOf(Math.max(...finalFitness))
    
    return {
      bestSchedule: population[bestIndex],
      fitness: finalFitness[bestIndex],
      efficiency: finalFitness[bestIndex] / (shifts.length * 10)
    }
  }
  
  /**
   * 模拟退火算法 - 部门重组优化
   * @param {Array} employees - 员工数组
   * @param {Array} departments - 部门数组
   * @param {Function} costFunction - 成本函数
   */
  const simulatedAnnealing = (employees, departments, costFunction) => {
    const initialTemp = 1000
    const finalTemp = 1
    const coolingRate = 0.95
    
    // 生成初始解
    let currentSolution = {}
    employees.forEach(emp => {
      const randomDept = departments[Math.floor(Math.random() * departments.length)]
      currentSolution[emp.id] = randomDept.id
    })
    
    let currentCost = costFunction(currentSolution, employees, departments)
    let bestSolution = { ...currentSolution }
    let bestCost = currentCost
    let temperature = initialTemp
    
    while (temperature > finalTemp) {
      // 生成邻近解
      const newSolution = { ...currentSolution }
      const randomEmployee = employees[Math.floor(Math.random() * employees.length)]
      const randomDepartment = departments[Math.floor(Math.random() * departments.length)]
      newSolution[randomEmployee.id] = randomDepartment.id
      
      const newCost = costFunction(newSolution, employees, departments)
      const deltaE = newCost - currentCost
      
      // 接受或拒绝新解
      if (deltaE < 0 || Math.random() < Math.exp(-deltaE / temperature)) {
        currentSolution = newSolution
        currentCost = newCost
        
        if (newCost < bestCost) {
          bestSolution = { ...newSolution }
          bestCost = newCost
        }
      }
      
      temperature *= coolingRate
    }
    
    return {
      bestSolution,
      bestCost,
      improvement: (costFunction({}, employees, departments) - bestCost) / costFunction({}, employees, departments)
    }
  }
  
  return {
    geneticAlgorithmScheduling,
    simulatedAnnealing
  }
} 