from relay_timer import RelayTimer


def test_complete_relay():
    print("=== 测试1: 完整接力，所有选手成功 ===")
    timer = RelayTimer(time_limit_per_runner=30)

    timer.results.append({"runner": "选手1", "leg": 1, "elapsed": 8.5, "status": "success"})
    timer.results.append({"runner": "选手2", "leg": 2, "elapsed": 7.2, "status": "success"})
    timer.results.append({"runner": "选手3", "leg": 3, "elapsed": 9.1, "status": "success"})
    timer.finished = True
    timer._print_results()
    print()


def test_foul_on_second_runner():
    print("=== 测试2: 第二棒选手犯规 ===")
    timer = RelayTimer(time_limit_per_runner=30)

    timer.results.append({"runner": "选手1", "leg": 1, "elapsed": 8.5, "status": "success"})
    timer.results.append({"runner": "选手2", "leg": 2, "elapsed": 3.2, "status": "failed", "reason": "犯规"})
    timer.failure_reason = "选手2 犯规"
    timer.finished = True
    timer._print_results()
    print()


def test_timeout_on_first_runner():
    print("=== 测试3: 第一棒选手超时 ===")
    timer = RelayTimer(time_limit_per_runner=10)

    timer.results.append({"runner": "选手1", "leg": 1, "elapsed": 10.5, "status": "failed", "reason": "超时(超过10秒)"})
    timer.failure_reason = "选手1 超时(超过10秒)"
    timer.finished = True
    timer._print_results()
    print()


def test_custom_names():
    print("=== 测试4: 自定义选手名称 ===")
    timer = RelayTimer(runner_names=["张三", "李四", "王五"], time_limit_per_runner=20)

    timer.results.append({"runner": "张三", "leg": 1, "elapsed": 6.5, "status": "success"})
    timer.results.append({"runner": "李四", "leg": 2, "elapsed": 5.8, "status": "success"})
    timer.results.append({"runner": "王五", "leg": 3, "elapsed": 7.1, "status": "success"})
    timer.finished = True
    timer._print_results()
    print()


def test_record_failure():
    print("=== 测试5: 测试失败记录逻辑 ===")
    timer = RelayTimer(time_limit_per_runner=30)
    timer._record_failure(1, "测试选手", 12.3, "抢跑犯规")

    assert len(timer.results) == 1
    assert timer.results[0]["status"] == "failed"
    assert timer.results[0]["reason"] == "抢跑犯规"
    assert timer.failure_reason == "测试选手 抢跑犯规"
    print("✓ 失败记录逻辑正确")
    print()


if __name__ == "__main__":
    test_complete_relay()
    test_foul_on_second_runner()
    test_timeout_on_first_runner()
    test_custom_names()
    test_record_failure()
    print("✅ 所有测试通过!")
