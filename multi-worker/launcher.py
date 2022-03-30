from manager import add_calculation_request, add_calculation_requests

# add_calculation_request.apply_async(queue='manager')
add_calculation_requests.apply_async(queue='manager')

