
def all_messages(mongo_mess, slack_mess):
    # For all messages on db set 'color' field as 'success' and add to new list
    #   for all messages on slack and not already on db set 'color' field as 
    #   'danger' and add to new list
    # return: list of dict sorted by timestamp
    # mongo_mess: list of dict 
    # slack_mess: list of dict
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
    # Save all messages in collection
    #   remove 'color' and 'ObjectId' fields
    # return: boolean
    # collection: pymongo collection
    # messages: list of dict
    saved = True 

    # No messages
    if not messages:
        return saved
    
    if isinstance(messages, list):
        for m in messages:
            if 'ObjectId' in m:
                m = remove_id(m)
            m = eval(m)
            if m['color'] == 'danger':
                del m['color']
                s = collection.insert_one(m)
                if not s.inserted_id:
                    saved = False

    return saved



def delete_messages(collection, messages):
    # Delete all messages from collection
    # return: boolean
    # collection: pymongo collection
    # massages: list of dict
    deleted = 0

    if not messages:
        return deleted

    if isinstance(messages, list):
        for m in messages:
            if 'ObjectId' in m:
                m = remove_id(m)
            m = eval(m)
            if m['color'] == 'success':
                del m['color']
                d = collection.delete_one(m)
                deleted += d.deleted_count

    return deleted == len(messages)

def remove_id(dict_string):
    # Remove '_id' field if it's still there
    # return: dict as string
    # dict_string: dict as string
    tab = dict_string.split(',')
    if '_id' in tab[0]:
        tab[1] = "{"+tab[1]
        del tab[0]
    elif '_id' in tab[-1]:
        tab[-2] = tab[-2]+"}"
        del tab[-1]
    else:
        tbr = None
        for i in range(1, len(tab)-1):
            if '_id' in tab[i]:
                tbr = i

        del tab[tbr]
    return ','.join(tab)
