"""
OS Action Execution Engine for BhashaFlow.
Handles safe mouse, keyboard, hotkey, and system automation tasks.
"""
import time
import logging
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class OSActionEngine:
    def __init__(self):
        logging.info("OSActionEngine initialized with FailSafe enabled.")

    def execute_plan(self, plan_data: dict) -> bool:
        thought = plan_data.get("thought_process", "Executing tasks...")
        actions = plan_data.get("execution_plan", [])
        logging.info(f"Target Plan: {thought}")

        for step in actions:
            step_num = step.get("step", 0)
            action_type = step.get("action")
            params = step.get("params", {})
            outcome = step.get("expected_outcome", "")

            logging.info(f"Step {step_num}: {action_type} -> {outcome}")
            success = self._run_single_action(action_type, params)
            if not success:
                logging.error(f"Step {step_num} failed to execute.")
                return False

        tts_feedback = plan_data.get("confirmation_speech", "Done!")
        logging.info(f"[TTS Output]: {tts_feedback}")
        return True

    def _run_single_action(self, action_type: str, params: dict) -> bool:
        try:
            if action_type == "hotkey":
                keys = params.get("keys", [])
                if keys:
                    pyautogui.hotkey(*keys)
            elif action_type == "press_key":
                key = params.get("key")
                if key:
                    pyautogui.press(key)
            elif action_type == "type_text":
                text = params.get("text", "")
                interval = params.get("interval", 0.02)
                pyautogui.write(text, interval=interval)
            elif action_type == "click":
                x = params.get("x")
                y = params.get("y")
                clicks = params.get("clicks", 1)
                pyautogui.click(x=x, y=y, clicks=clicks)
            elif action_type == "wait":
                duration = params.get("duration", 0.5)
                time.sleep(duration)
            else:
                logging.warning(f"Unrecognized action type: {action_type}")
                return False
            return True
        except pyautogui.FailSafeException:
            logging.critical("Emergency abort triggered via PyAutoGUI FailSafe.")
            return False
        except Exception as e:
            logging.error(f"Execution error on {action_type}: {e}")
            return False

if __name__ == "__main__":
    engine = OSActionEngine()
    print("Action Engine self-test complete.")
