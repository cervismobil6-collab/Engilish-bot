#!/usr/bin/env python3
"""
Auto-restart wrapper for bot (24/7 running)
If bot crashes, it will automatically restart
"""

import subprocess
import logging
import time
import os
import signal
import sys
from datetime import datetime

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

MAX_RESTARTS = 5
RESTART_DELAY = 5  # seconds


class BotManager:
    """Manage bot process with auto-restart"""
    
    def __init__(self):
        self.process = None
        self.restart_count = 0
        self.last_restart = None
    
    def start_bot(self):
        """Start bot process"""
        try:
            logger.info("="*60)
            logger.info(f"🤖 Bot ishga tushirilmoqda... ({self.restart_count + 1}-chi urinish)")
            logger.info(f"⏰ Vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info("="*60)
            
            self.process = subprocess.Popen(
                ['python3', 'server.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.last_restart = datetime.now()
            self.restart_count += 1
            
            logger.info(f"✅ Bot process (PID: {self.process.pid}) ishga tushdi")
            return True
        
        except Exception as e:
            logger.error(f"❌ Bot ishga tushurilmadi: {e}")
            return False
    
    def handle_process_output(self):
        """Handle bot process output"""
        try:
            while self.process and self.process.poll() is None:
                # Log stdout
                if self.process.stdout:
                    line = self.process.stdout.readline()
                    if line:
                        logger.info(f"[BOT] {line.strip()}")
                
                time.sleep(0.1)
        
        except Exception as e:
            logger.error(f"Output handler xatosi: {e}")
    
    def monitor(self):
        """Monitor and restart bot if crashed"""
        while True:
            try:
                if not self.start_bot():
                    logger.error("❌ Bot ishga tushurilmadi!")
                    time.sleep(RESTART_DELAY)
                    continue
                
                # Wait for process to finish
                exit_code = self.process.wait()
                
                if exit_code != 0:
                    logger.warning(
                        f"⚠️  Bot to'xtadi (exit code: {exit_code})"
                    )
                else:
                    logger.info("Bot to'xtadi (normal)")
                
                if self.restart_count >= MAX_RESTARTS:
                    logger.critical(
                        f"❌ Maksimal restart soniga ({MAX_RESTARTS}) yetdi!"
                    )
                    break
                
                logger.info(
                    f"⏳ {RESTART_DELAY} soniyadan keyin qayta ishga tushuriladi..."
                )
                time.sleep(RESTART_DELAY)
            
            except KeyboardInterrupt:
                logger.info("\n⛔ Manager to'xtatildi")
                if self.process:
                    self.process.terminate()
                    self.process.wait()
                break
            
            except Exception as e:
                logger.error(f"Monitor xatosi: {e}")
                time.sleep(RESTART_DELAY)
    
    def shutdown(self):
        """Graceful shutdown"""
        logger.info("🛑 Graceful shutdown boshlandi...")
        
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logger.warning("⚠️  Process to'xtamadi, force kill ishga tushdirilyapti...")
                self.process.kill()
        
        logger.info("✅ Shutdown tugadi")


def signal_handler(signum, frame):
    """Handle termination signals"""
    logger.info(f"\n📞 Signal {signum} qabul qilindi")
    manager.shutdown()
    sys.exit(0)


if __name__ == "__main__":
    logger.info("\n" + "="*60)
    logger.info("🔥 BOT MANAGER - 24/7 AUTO-RESTART")
    logger.info("="*60 + "\n")
    
    manager = BotManager()
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start monitoring
    try:
        manager.monitor()
    except Exception as e:
        logger.critical(f"Kritik xatolik: {e}")
        sys.exit(1)
