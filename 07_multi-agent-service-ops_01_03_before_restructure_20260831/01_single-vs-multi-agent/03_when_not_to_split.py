"""역할 이름을 늘리는 것과 책임을 분리하는 것은 다릅니다."""


def one_clear_responsibility(box_count: int) -> dict:
    return {
        "box_count": box_count,
        "label_count": box_count,
        "summary": f"상자 {box_count}개에 라벨 {box_count}개가 필요합니다.",
    }


def unnecessarily_split(box_count: int) -> dict:
    counter_result = {"box_count": box_count}
    label_result = {"label_count": counter_result["box_count"]}
    summary_result = {
        "summary": f"상자 {counter_result['box_count']}개에 "
        f"라벨 {label_result['label_count']}개가 필요합니다."
    }
    return {**counter_result, **label_result, **summary_result}


def compare_designs(box_count: int) -> dict:
    single = one_clear_responsibility(box_count)
    split = unnecessarily_split(box_count)
    return {
        "same_result": single == split,
        "single_calls": 1,
        "split_calls": 3,
        "decision": "책임과 데이터가 분리되지 않으므로 하나의 함수가 더 단순합니다.",
    }


if __name__ == "__main__":
    print(compare_designs(15))
