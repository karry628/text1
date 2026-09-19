# 五岔路口交通灯相位设计 - 图着色算法实现
# 路口方向顺时针顺序：A(下) → E(右下) → D(右上) → C(上) → B(左) → A
# 单行道规则：C只能作为出口（不可驶入），E只能作为入口（不可驶出）

# 方向到索引的映射（顺时针编号）
points = {'A': 0, 'E': 1, 'D': 2, 'C': 3, 'B': 4}
idx_to_point = {v: k for k, v in points.items()}

def generate_all_routes():
    """生成所有合法的通行路线，共13条"""
    entrances = ['A', 'B', 'D', 'E']  # 可驶入路口的方向（C是单行道出口，不能进）
    exits = ['A', 'B', 'C', 'D']      # 可驶出路口的方向（E是单行道入口，不能出）
    routes = []
    for start in entrances:
        for end in exits:
            if start != end:  # 排除同方向掉头
                routes.append( (start, end) )
    return routes

def is_conflict(route1, route2):
    """
    判断两条路线是否冲突（行驶轨迹交叉，不能同时通行）
    原理：环形路口中，两条路线交叉 等价于 起点和终点在环上交替分布
    """
    s1, e1 = route1
    s2, e2 = route2
    s1_idx, e1_idx = points[s1], points[e1]
    s2_idx, e2_idx = points[s2], points[e2]

    # 有公共起点/终点的路线不冲突（比如同起点的车流可以一起放行）
    if s1_idx == s2_idx or e1_idx == e2_idx or s1_idx == e2_idx or e1_idx == s2_idx:
        return False

    # 判断点p是否在s到e的顺时针开区间内
    def in_clockwise(s, e, p):
        if s < e:
            return s < p < e
        else:  # 区间跨过0号点
            return p > s or p < e

    # 两个端点一个在弧内、一个在弧外 → 交替分布 → 路线交叉
    s2_in = in_clockwise(s1_idx, e1_idx, s2_idx)
    e2_in = in_clockwise(s1_idx, e1_idx, e2_idx)
    return s2_in != e2_in

def build_conflict_graph(routes):
    """构建冲突图：顶点=路线，边=两条路线冲突"""
    n = len(routes)
    adjacency = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if is_conflict(routes[i], routes[j]):
                adjacency[i].append(j)
                adjacency[j].append(i)
    return adjacency

def greedy_graph_coloring(adjacency):
    """贪心图着色算法：按顶点度数从大到小着色，求最少颜色数（相位）"""
    n = len(adjacency)
    # 按度数降序排序顶点，优化着色效果
    vertices = sorted(range(n), key=lambda x: len(adjacency[x]), reverse=True)
    color = [-1] * n
    color[vertices[0]] = 0  # 第一个顶点着色0

    for u in vertices[1:]:
        # 收集相邻顶点已使用的颜色
        used_colors = set()
        for v in adjacency[u]:
            if color[v] != -1:
                used_colors.add(color[v])
        # 选择最小的可用颜色
        c = 0
        while c in used_colors:
            c += 1
        color[u] = c
    return color

def print_solution(routes, color_result):
    """输出最终的信号灯相位方案"""
    phases = {}
    for idx, c in enumerate(color_result):
        if c not in phases:
            phases[c] = []
        phases[c].append(f"{routes[idx][0]}→{routes[idx][1]}")
    
    print("="*50)
    print("五岔路口信号灯相位方案")
    print("="*50)
    for phase_id in sorted(phases.keys()):
        print(f"相位 {phase_id+1}（绿灯放行）：{', '.join(phases[phase_id])}")
    print(f"\n最少需要 {len(phases)} 个信号灯相位")

def verify_examples():
    """验证题目给出的示例是否符合预期"""
    print("\n" + "="*50)
    print("题目示例验证")
    print("="*50)
    r_eb = ('E', 'B')
    r_ad = ('A', 'D')
    print(f"E→B 与 A→D 是否冲突：{is_conflict(r_eb, r_ad)} （题目说明：不可同时通行 → 预期True）")

    r_ab = ('A', 'B')
    r_ec = ('E', 'C')
    print(f"A→B 与 E→C 是否冲突：{is_conflict(r_ab, r_ec)} （题目说明：可以同时通行 → 预期False）")

if __name__ == "__main__":
    # 1. 生成所有合法路线
    all_routes = generate_all_routes()
    print(f"总共有 {len(all_routes)} 条可通行路线")

    # 2. 构建冲突图
    conflict_graph = build_conflict_graph(all_routes)

    # 3. 图着色求解
    color_result = greedy_graph_coloring(conflict_graph)

    # 4. 输出方案
    print_solution(all_routes, color_result)

    # 5. 验证题目示例
    verify_examples()
