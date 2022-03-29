from manager import add_calculation_request

add_calculation_request.apply_async(queue='manager')
