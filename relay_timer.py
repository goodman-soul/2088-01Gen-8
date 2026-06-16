import time
import sys
import io


class RelayTimer:
    DISPLAY_INTERVAL = 1.0

    def __init__(self, runner_names=None, time_limit_per_runner=30):
        self.runner_names = runner_names or ["选手1", "选手2", "选手3"]
        self.time_limit = time_limit_per_runner
        self.results = []
        self.failure_reason = None
        self.finished = False
        self._cancelled = False

    def run(self):
        print("=" * 50)
        print("🏃 三人接力计时器 🏃")
        print("=" * 50)
        print(f"每位选手时限: {self.time_limit} 秒")
        print(f"选手顺序: {' → '.join(self.runner_names)}")
        print("-" * 50)

        for i, runner in enumerate(self.runner_names):
            if self.failure_reason or self._cancelled:
                break

            print(f"\n第 {i + 1} 棒: {runner} 准备出发...")
            try:
                input("按回车键开始...")
            except (EOFError, KeyboardInterrupt):
                self._cancelled = True
                elapsed = 0.0
                self._record_failure(i, runner, elapsed, "用户取消")
                break

            start_time = time.time()
            print(f"{runner} 已出发！(计时中...)")

            try:
                result = self._wait_for_finish(runner, start_time)
            except KeyboardInterrupt:
                elapsed = time.time() - start_time
                self._record_failure(i, runner, elapsed, "手动中断(犯规)")
                break
            except EOFError:
                elapsed = time.time() - start_time
                self._record_failure(i, runner, elapsed, "输入结束(用户取消)")
                break

            if result["status"] == "success":
                self.results.append({
                    "runner": runner,
                    "leg": i + 1,
                    "elapsed": result["elapsed"],
                    "status": "success"
                })
                print(f"\n✅ {runner} 完成! 用时: {result['elapsed']:.2f} 秒")
                if i < len(self.runner_names) - 1:
                    print(f"交棒给下一位选手...")
            elif result["status"] == "foul":
                self._record_failure(i, runner, result["elapsed"], "犯规")
                break
            elif result["status"] == "timeout":
                self._record_failure(i, runner, result["elapsed"], f"超时(超过{self.time_limit}秒)")
                break

        self.finished = True
        self._print_results()

    def _wait_for_finish(self, runner, start_time):
        last_display = 0.0
        use_select = True
        try:
            import select
            select.select([sys.stdin], [], [], 0)
        except (ImportError, io.UnsupportedOperation, AttributeError, ValueError, OSError):
            use_select = False

        while True:
            elapsed = time.time() - start_time

            if elapsed >= self.time_limit:
                print()
                return {"status": "timeout", "elapsed": elapsed}

            if elapsed - last_display >= self.DISPLAY_INTERVAL:
                print(f"\r⏱  已用时: {elapsed:5.1f} 秒  |  输入 f=犯规, s=成功, 等待中...", end="", flush=True)
                last_display = elapsed

            if use_select:
                import select
                ready, _, _ = select.select([sys.stdin], [], [], 0.1)
                if not ready:
                    continue
            else:
                if not sys.stdin.readable():
                    time.sleep(0.1)
                    continue

            user_input = sys.stdin.readline()
            if not user_input:
                raise EOFError()
            user_input = user_input.strip().lower()
            if user_input == 'f':
                return {"status": "foul", "elapsed": elapsed}
            elif user_input == 's':
                return {"status": "success", "elapsed": elapsed}

    def _record_failure(self, index, runner, elapsed, reason):
        self.results.append({
            "runner": runner,
            "leg": index + 1,
            "elapsed": elapsed,
            "status": "failed",
            "reason": reason
        })
        self.failure_reason = f"{runner} {reason}"
        print(f"\n❌ {self.failure_reason}! 接力停止。")

    def _print_results(self):
        print("\n" + "=" * 50)
        print("📊 接力结果")
        print("=" * 50)

        total_time = 0.0
        for r in self.results:
            status_icon = "✅" if r["status"] == "success" else "❌"
            extra = f" ({r['reason']})" if r["status"] == "failed" else ""
            print(f"{status_icon} 第{r['leg']}棒 {r['runner']}: {r['elapsed']:.2f} 秒{extra}")
            if r["status"] == "success":
                total_time += r["elapsed"]

        print("-" * 50)
        if self.failure_reason:
            print(f"🏁 接力失败: {self.failure_reason}")
            uncompleted = len(self.runner_names) - len(self.results)
            if uncompleted > 0:
                remaining = ", ".join(self.runner_names[-uncompleted:])
                print(f"⏭  未出场选手: {remaining}")
        else:
            print(f"🎉 接力完成! 总用时: {total_time:.2f} 秒")
        print("=" * 50)


def main():
    import sys
    if len(sys.argv) > 1:
        names = sys.argv[1:4] if len(sys.argv) >= 4 else sys.argv[1:]
        while len(names) < 3:
            names.append(f"选手{len(names) + 1}")
    else:
        names = None

    timer = RelayTimer(runner_names=names)
    timer.run()


if __name__ == "__main__":
    main()
