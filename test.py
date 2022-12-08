
store = store
current_element = p
flag = True
total = 0

while True:
    if store in current_element.account_id:
        total = total + current_element.value
    
    if current_element.next == None:
        break
    
    current_element = current_element.next
        