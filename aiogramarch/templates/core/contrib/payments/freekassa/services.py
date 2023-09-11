import hashlib

from .schemas import SuccessPay


def generate_callback_signature(
		merchant_id,
		amount,
		seckret2,
		merchant_order_id) -> str:
	params = [merchant_id, amount, seckret2, merchant_order_id]
	params = [str(param) for param in params]
	sign = ':'.join(params)
	return hashlib.md5(sign.encode('utf-8')).hexdigest()


def success_SIGN(
	success_pay: SuccessPay,
	merchant_id: int,
    amount: int,
    seckret2: str,
    merchant_order_id: int,
) -> bool:
    SIGN = success_pay["SIGN"]
    generated_SIGN = generate_callback_signature(
        merchant_id=merchant_id,
        amount=amount,
        seckret2=seckret2,
        merchant_order_id=merchant_order_id,
    )

    if SIGN == generated_SIGN:
        return True
