"""
Payment processing module
"""

import logging
from typing import Optional, Dict
from datetime import datetime, timedelta
from database.queries import update_user_premium
from config import config

logger = logging.getLogger(__name__)


class PaymentProcessor:
    """Handle payment processing"""
    
    @staticmethod
    async def process_payme_payment(payment_id: str, amount: int, user_id: int) -> bool:
        """
        Process Payme payment
        """
        try:
            # Verify with Payme API
            # TODO: Implement actual Payme API integration
            logger.info(f"Processing Payme payment: {payment_id} - {amount} som")
            
            # Determine premium plan based on amount
            plan = PaymentProcessor._get_plan_by_amount(amount)
            if plan:
                await update_user_premium(user_id, plan)
                logger.info(f"User {user_id} upgraded to {plan}")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Payme payment error: {e}")
            return False
    
    @staticmethod
    async def process_click_payment(transaction_id: str, amount: int, user_id: int) -> bool:
        """
        Process Click payment
        """
        try:
            # Verify with Click API
            # TODO: Implement actual Click API integration
            logger.info(f"Processing Click payment: {transaction_id} - {amount} som")
            
            # Determine premium plan based on amount
            plan = PaymentProcessor._get_plan_by_amount(amount)
            if plan:
                await update_user_premium(user_id, plan)
                logger.info(f"User {user_id} upgraded to {plan}")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Click payment error: {e}")
            return False
    
    @staticmethod
    def _get_plan_by_amount(amount: int) -> Optional[str]:
        """
        Determine premium plan based on payment amount
        """
        if amount == config.PREMIUM_PRICE_1MONTH:
            return '1month'
        elif amount == config.PREMIUM_PRICE_3MONTH:
            return '3months'
        elif amount == config.PREMIUM_PRICE_LIFETIME:
            return 'lifetime'
        return None
