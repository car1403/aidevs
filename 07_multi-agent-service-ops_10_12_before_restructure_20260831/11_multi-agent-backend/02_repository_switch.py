def select_storage(mode: str) -> str:
    if mode not in {"memory", "redis"}:
        raise ValueError("STORAGE_MODE는 memory 또는 redis여야 합니다.")
    return "설치 없이 학습" if mode == "memory" else "여러 Process가 공유"


if __name__ == "__main__":
    print("Memory:", select_storage("memory"))
    print("Redis:", select_storage("redis"))
