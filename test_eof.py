from relay_timer import RelayTimer
import sys
import io


def test_eof_at_start():
    print("=== 测试: 第一棒开始前遇到 EOF (Ctrl+D) ===")
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO("")
        timer = RelayTimer(time_limit_per_runner=10)
        timer.run()
        assert timer.failure_reason is not None
        assert "用户取消" in timer.failure_reason
        print("✓ 第一棒 EOF 处理正确")
    finally:
        sys.stdin = old_stdin
    print()


def test_eof_at_second_runner():
    print("=== 测试: 第二棒开始前遇到 EOF ===")
    old_stdin = sys.stdin
    try:
        test_input = "\ns\n"
        sys.stdin = io.StringIO(test_input)
        timer = RelayTimer(time_limit_per_runner=10)
        timer.run()
        assert len(timer.results) >= 1
        assert timer.results[0]["status"] == "success"
        assert timer.failure_reason is not None
        assert "选手2" in timer.failure_reason
        print("✓ 第二棒 EOF 处理正确")
    finally:
        sys.stdin = old_stdin
    print()


def test_eof_during_waiting():
    print("=== 测试: 计时中遇到 EOF ===")
    old_stdin = sys.stdin
    old_select = __import__("select").select

    def fake_select(rlist, wlist, xlist, timeout=0):
        if rlist and rlist[0] is sys.stdin:
            return ([sys.stdin], [], [])
        return ([], [], [])

    try:
        import select
        select.select = fake_select
        sys.stdin = io.StringIO("\ns\nf")
        timer = RelayTimer(time_limit_per_runner=10)
        timer.run()
        print("✓ 计时中 EOF 不会导致崩溃")
    finally:
        sys.stdin = old_stdin
        select.select = old_select
    print()


if __name__ == "__main__":
    test_eof_at_start()
    test_eof_at_second_runner()
    test_eof_during_waiting()
    print("✅ 所有 EOF 相关测试通过!")
