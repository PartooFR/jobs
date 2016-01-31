
def all_messages(mongo_mess, slack_mess):
    messages = {}

    for m in mongo_mess:
        m['color'] = 'success'
        messages[m['ts']] = m

    for m in slack_mess:
        if m['ts'] not in messages:
            m['color'] = 'danger'
            messages[m['ts']] = m

    ret = list(messages.values())
    return list(reversed(sorted(ret, key=lambda msg: msg['ts'])))

def save_messages(collection, messages):
    saved = False

    # No messages
    if not messages:
        return saved
    
    if isinstance(messages, list):
        for m in messages:
            m = eval(m)
            if m['color'] == 'danger':
                del m['color']
                saved = collection.save(m)

    return saved

def delete_messages(collection, messages):
    deleted = False

    if not messages:
        return deleted

    if isinstance(messages, list):
        for m in messages:
            if 'ObjectId' in m:
                m = remove_id(m)
            m = eval(m)
            if m['color'] == 'success':
                del m['color']
                deleted = collection.remove(m)

    return deleted

def remove_id(dict_string):
    tab = dict_string.split(',')
    if '_id' in tab[0]:
        tab[1] = "{"+tab[1]
    elif '_id' in tab[-1]:
        tab[-2] = tab[-2]+"}"
    else:
        tbr = None
        for i in range(1, len(tab)-1):
            if '_id' in tab[i]:
                tbr = i

        del tab[tbr]
    return ','.join(tab)
