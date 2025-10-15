# career_evaluator_interactive.py

def get_criteria():
    n = int(input("请输入评分指标的数量："))
    criteria = []
    for i in range(n):
        name = input(f"请输入第 {i+1} 个指标名称：")
        criteria.append(name)
    return criteria


def get_weights(criteria):
    print("\n请输入各指标的权重（总和建议为1，可自动归一化）：")
    weights = []
    for name in criteria:
        w = float(input(f"权重 - {name}: "))
        weights.append(w)

    # 自动归一化处理
    total = sum(weights)
    if total != 0:
        weights = [w / total for w in weights]
    print("\n权重已归一化为：", [round(w, 3) for w in weights])
    return weights


def get_options(criteria):
    m = int(input("\n请输入要评估的对象数量："))
    options = {}
    for i in range(m):
        name = input(f"\n请输入第 {i+1} 个对象名称：")
        scores = []
        for c in criteria:
            s = float(input(f"请输入 {name} 的 {c} 得分（0~10）："))
            scores.append(s)
        options[name] = scores
    return options


def evaluate(options, weights):
    results = {}
    for name, scores in options.items():
        total = sum(s * w for s, w in zip(scores, weights))
        results[name] = total
    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))


def main():
    print("==== 欢迎使用智能评分系统 ====\n")
    criteria = get_criteria()
    weights = get_weights(criteria)
    options = get_options(criteria)

    results = evaluate(options, weights)

    print("\n==== 最终得分与排名 ====")
    for i, (name, score) in enumerate(results.items(), start=1):
        print(f"{i}. {name}: {score:.2f}")


if __name__ == "__main__":
    main()
