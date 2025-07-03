/**
 * 用于部门层级管理和薪资路径优化
 */

export const useGraphAlgorithms = () => {
  
  /**
   * Dijkstra算法 - 寻找部门间最短晋升路径
   * @param {Object} graph - 部门关系图
   * @param {string} start - 起始部门
   * @param {string} end - 目标部门
   */
  /**
   * Dijkstra算法实现 - 用于计算图中两点间最短路径
   * @param {Object} graph - 部门关系图，格式为 {部门A: {部门B: 距离, ...}, ...}
   * @param {string} start - 起始部门名称
   * @param {string} end - 目标部门名称
   */
  const dijkstra = (graph, start, end) => {
    // 存储从起点到各节点的最短距离
    const distances = {}
    // 存储路径中每个节点的前驱节点
    const previous = {}
    // 未访问节点集合
    const unvisited = new Set()
    
    // 初始化所有节点
    for (const node in graph) {
      // 起点距离设为0，其他设为无穷大
      distances[node] = node === start ? 0 : Infinity
      // 前驱节点初始为null
      previous[node] = null
      // 所有节点加入未访问集合
      unvisited.add(node)
    }
    
    // 主循环，直到所有节点都被访问
    while (unvisited.size > 0) {
      // 在未访问节点中找到距离最小的节点
      const current = Array.from(unvisited).reduce((min, node) => 
        distances[node] < distances[min] ? node : min
      )
      
      // 将当前节点标记为已访问
      unvisited.delete(current)
      
      // 如果到达目标节点，提前结束
      if (current === end) break
      
      // 遍历当前节点的所有邻居
      for (const neighbor in graph[current]) {
        // 只处理未访问的邻居
        if (unvisited.has(neighbor)) {
          // 计算通过当前节点到达邻居的新距离
          const newDist = distances[current] + graph[current][neighbor]
          // 如果新距离更短，则更新
          if (newDist < distances[neighbor]) {
            distances[neighbor] = newDist
            previous[neighbor] = current  // 记录路径
          }
        }
      }
    }
    
    // 构建路径
    // 初始化路径数组
    const path = []
    // 从终点开始回溯路径
    let current = end
    
    // 循环回溯路径，直到起点(current为null时停止)
    while (current !== null) {
      // 将当前节点添加到路径数组的开头(保证路径顺序正确)
      path.unshift(current)
      // 移动到前驱节点继续回溯
      current = previous[current]
    }
    
    // 返回结果对象
    return {
      // 起点到终点的最短距离
      distance: distances[end],
      // 如果存在有效路径则返回路径数组，否则返回空数组
      path: distances[end] !== Infinity ? path : [],
      // 包含所有节点到起点的最短距离
      allDistances: distances
    }
  }
  
  /**
   * Floyd-Warshall算法 - 计算所有部门间的最短路径
   * @param {Object} graph - 部门关系图
   */
  const floydWarshall = (graph) => {
    const nodes = Object.keys(graph)
    const dist = {}
    const next = {}
    
    // 初始化距离矩阵
    for (const i of nodes) {
      dist[i] = {}
      next[i] = {}
      for (const j of nodes) {
        if (i === j) {
          dist[i][j] = 0
        } else if (graph[i] && graph[i][j]) {
          dist[i][j] = graph[i][j]
          next[i][j] = j
        } else {
          dist[i][j] = Infinity
        }
      }
    }
    
    // Floyd-Warshall核心算法
    for (const k of nodes) {
      for (const i of nodes) {
        for (const j of nodes) {
          if (dist[i][k] + dist[k][j] < dist[i][j]) {
            dist[i][j] = dist[i][k] + dist[k][j]
            next[i][j] = next[i][k]
          }
        }
      }
    }
    
    return { distances: dist, next }
  }
  
  /**
   * 构建部门层级图
   * @param {Array} departments - 部门数据
   * @param {Array} employees - 员工数据
   */
  const buildDepartmentGraph = (departments, employees) => {
    const graph = {}
    const departmentMap = {}
    
    // 创建部门映射
    departments.forEach(dept => {
      departmentMap[dept.name] = dept
      graph[dept.name] = {}
    })
    
    // 基于薪资水平和职级建立连接
    departments.forEach(dept => {
      const deptEmployees = employees.filter(emp => emp.department === dept.name)
      const avgSalary = calculateAverageSalary(deptEmployees)
      
      departments.forEach(targetDept => {
        if (dept.name !== targetDept.name) {
          const targetEmployees = employees.filter(emp => emp.department === targetDept.name)
          const targetAvgSalary = calculateAverageSalary(targetEmployees)
          
          // 计算晋升难度（基于薪资差异和职级要求）
          const salaryDiff = Math.abs(targetAvgSalary - avgSalary)
          const difficulty = calculatePromotionDifficulty(dept, targetDept, salaryDiff)
          
          if (difficulty < Infinity) {
            graph[dept.name][targetDept.name] = difficulty
          }
        }
      })
    })
    
    return graph
  }
  
  /**
   * 计算平均薪资
   */
  const calculateAverageSalary = (employees) => {
    if (!employees.length) return 0
    const total = employees.reduce((sum, emp) => sum + (emp.base_salary || 0), 0)
    return total / employees.length
  }
  
  /**
   * 计算晋升难度
   */
  const calculatePromotionDifficulty = (fromDept, toDept, salaryDiff) => {
    // 基础难度
    let difficulty = 1
    
    // 薪资差异影响
    difficulty += salaryDiff / 1000
    
    // 部门性质影响
    const techDepts = ['技术部', '研发部', '产品部']
    const managementDepts = ['人事部', '行政部', '财务部']
    
    if (techDepts.includes(fromDept.name) && managementDepts.includes(toDept.name)) {
      difficulty += 2 // 技术转管理较难
    }
    
    if (managementDepts.includes(fromDept.name) && techDepts.includes(toDept.name)) {
      difficulty += 3 // 管理转技术更难
    }
    
    return difficulty
  }
  
  /**
   * 寻找最佳晋升路径
   * @param {Array} departments - 部门数据
   * @param {Array} employees - 员工数据
   * @param {string} currentDept - 当前部门
   * @param {string} targetDept - 目标部门
   */
  const findOptimalCareerPath = (departments, employees, currentDept, targetDept) => {
    const graph = buildDepartmentGraph(departments, employees)
    const result = dijkstra(graph, currentDept, targetDept)
    
    // 为路径添加详细信息
    const detailedPath = result.path.map((deptName, index) => {
      const dept = departments.find(d => d.name === deptName)
      const deptEmployees = employees.filter(emp => emp.department === deptName)
      
      return {
        department: deptName,
        averageSalary: calculateAverageSalary(deptEmployees),
        employeeCount: deptEmployees.length,
        step: index + 1,
        isTarget: index === result.path.length - 1,
        difficulty: index > 0 ? graph[result.path[index - 1]][deptName] : 0
      }
    })
    
    return {
      ...result,
      detailedPath,
      totalDifficulty: result.distance,
      recommendations: generateCareerRecommendations(detailedPath)
    }
  }
  
  /**
   * 生成职业发展建议
   */
  const generateCareerRecommendations = (path) => {
    const recommendations = []
    
    for (let i = 1; i < path.length; i++) {
      const from = path[i - 1]
      const to = path[i]
      
      recommendations.push({
        step: i,
        from: from.department,
        to: to.department,
        salaryIncrease: to.averageSalary - from.averageSalary,
        difficulty: to.difficulty,
        suggestions: [
          `提升${to.department}相关技能`,
          `建立${to.department}人脉关系`,
          `参与跨部门项目`,
          `考虑相关认证或培训`
        ]
      })
    }
    
    return recommendations
  }
  
  return {
    dijkstra,
    floydWarshall,
    buildDepartmentGraph,
    findOptimalCareerPath,
    generateCareerRecommendations
  }
}

/**
 * 最小生成树算法 - 优化部门间协作关系
 */
export const useMinimumSpanningTree = () => {
  
  /**
   * Kruskal算法 - 找到最小生成树
   * @param {Array} edges - 边的数组 [{from, to, weight}]
   * @param {Array} vertices - 顶点数组
   */
  const kruskal = (edges, vertices) => {
    // 按权重排序边
    const sortedEdges = [...edges].sort((a, b) => a.weight - b.weight)
    const parent = {}
    const rank = {}
    const mst = []
    
    // 初始化并查集
    vertices.forEach(v => {
      parent[v] = v
      rank[v] = 0
    })
    
    const find = (x) => {
      if (parent[x] !== x) {
        parent[x] = find(parent[x])
      }
      return parent[x]
    }
    
    const union = (x, y) => {
      const rootX = find(x)
      const rootY = find(y)
      
      if (rootX !== rootY) {
        if (rank[rootX] < rank[rootY]) {
          parent[rootX] = rootY
        } else if (rank[rootX] > rank[rootY]) {
          parent[rootY] = rootX
        } else {
          parent[rootY] = rootX
          rank[rootX]++
        }
        return true
      }
      return false
    }
    
    // 构建最小生成树
    for (const edge of sortedEdges) {
      if (union(edge.from, edge.to)) {
        mst.push(edge)
        if (mst.length === vertices.length - 1) break
      }
    }
    
    return mst
  }
  
  /**
   * 构建部门协作网络
   * @param {Array} departments - 部门数据
   * @param {Array} projects - 项目数据（包含跨部门协作信息）
   */
  const buildCollaborationNetwork = (departments, projects) => {
    const edges = []
    const vertices = departments.map(d => d.name)
    
    // 基于项目协作频率构建边
    departments.forEach(dept1 => {
      departments.forEach(dept2 => {
        if (dept1.name !== dept2.name) {
          const collaborationWeight = calculateCollaborationWeight(
            dept1.name, 
            dept2.name, 
            projects
          )
          
          if (collaborationWeight > 0) {
            edges.push({
              from: dept1.name,
              to: dept2.name,
              weight: collaborationWeight
            })
          }
        }
      })
    })
    
    return { edges, vertices }
  }
  
  /**
   * 计算部门间协作权重
   */
  const calculateCollaborationWeight = (dept1, dept2, projects) => {
    let weight = 0
    
    projects.forEach(project => {
      const dept1Involved = project.departments?.includes(dept1)
      const dept2Involved = project.departments?.includes(dept2)
      
      if (dept1Involved && dept2Involved) {
        // 基于项目重要性和持续时间计算权重
        weight += (project.priority || 1) * (project.duration || 1)
      }
    })
    
    return weight
  }
  
  /**
   * 优化部门协作结构
   * @param {Array} departments - 部门数据
   * @param {Array} projects - 项目数据
   */
  const optimizeCollaboration = (departments, projects) => {
    const { edges, vertices } = buildCollaborationNetwork(departments, projects)
    const mst = kruskal(edges, vertices)
    
    return {
      optimalCollaborations: mst,
      totalCollaborationCost: mst.reduce((sum, edge) => sum + edge.weight, 0),
      recommendations: generateCollaborationRecommendations(mst, departments)
    }
  }
  
  /**
   * 生成协作优化建议
   */
  const generateCollaborationRecommendations = (mst, departments) => {
    return mst.map(edge => ({
      departments: [edge.from, edge.to],
      collaborationStrength: edge.weight,
      suggestions: [
        '建立定期沟通机制',
        '设立跨部门联络人',
        '共享资源和工具',
        '制定协作流程标准'
      ]
    }))
  }
  
  return {
    kruskal,
    buildCollaborationNetwork,
    optimizeCollaboration,
    generateCollaborationRecommendations
  }
} 