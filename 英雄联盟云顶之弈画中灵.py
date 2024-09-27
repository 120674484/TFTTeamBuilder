import json
def bonds_deal(text):
    data =json.loads(text)
    bonds = []
    number_of_bonds = []
    for item in data['data']:
        if item['characterid']:
            bonds.append(item['name'])
            number_of_bonds.append([int(key) for key in reversed(list(item['level'].keys()))])
    return bonds,number_of_bonds
def chesses_deal(text):
    data=json.loads(text)
    names = []
    hero_bonds = []
    prices = []
    for item in data['data']:
        if int(item['price']) > 0 and item['displayName']!='霞洛':
            names.append(item['displayName'])
            if item['races']:
                races = item['races'].split(',')
            else:
                races = []
            if item['jobs']:
                jobs = item['jobs'].split(',')
            else:
                jobs = []
            hero_bonds.append(races + jobs)
            prices.append(int(item['price']))
    sizes = [1] * len(names)
    combined_heroes_index = []
    for hero_index in range(len(names)):
        if names[hero_index] in ['霞', '洛']:
            combined_heroes_index.append(hero_index)
    return names,hero_bonds,prices,sizes,combined_heroes_index
if __name__ == "__main__":
    from threading import Thread, Semaphore
    import copy,asyncio,aiohttp
    from multiprocessing import Pool
    def print_index_if_value_is_larger(lst, target_value):
        n = len(lst)
        if n > 0:
            for i in range(n):
                start = lst[i].find('(')
                end = lst[i].find(')')
                number = int(lst[i][start + 1:end])
                if target_value > number:
                    return i
            return n
        return 0
    def final_generate(thread_count, bond, population):
        bonds_group = {}
        original_hero_group = []
        values_list_best = []
        values_list_rest_best = []
        hero_numbers = []
        for j in range(len(names)):
            for a in hero_bonds[j]:
                if a == bond:
                    hero_numbers.append(j)
                    population -= sizes[j]
                    original_hero_group.insert(print_index_if_value_is_larger(original_hero_group, prices[j]),f'{names[j]}({prices[j]})')
                    for c in hero_bonds[j]:
                        try:
                            bonds_group[c] += 1
                        except:
                            bonds_group[c] = 1
                    break
        price_sum_max = 0
        if bond == '天龙之子':
            population += 1
            for p in combined_heroes_index:
                original_hero_group_copy = original_hero_group[:]
                original_hero_group_copy.remove(names[p] + '(' + str(prices[p]) + ')')
                bonds_dict = copy.deepcopy(bonds_group)
                for c in hero_bonds[p]:
                    bonds_dict[c] -= 1
                    if bonds_dict[c] == 0:
                        del bonds_dict[c]
                heroes_numbers_copy = hero_numbers[:]
                heroes_numbers_copy.remove(p)
                function1 = hero_group_generate(population, bonds_dict, heroes_numbers_copy,price_sum_max, values_list_best, values_list_rest_best)
                flag = function1['flag']
                heroes_groups = function1['heroes_groups']
                price_sum_max = function1['price_sum_max']
                values_list_best = function1['values_list_best']
                values_list_rest_best = function1['values_list_rest_best']
                if flag:
                    original_hero_group_list = [original_hero_group_copy]
                    heroes_groups_list = [heroes_groups]
                elif heroes_groups:
                    original_hero_group_list.append(original_hero_group_copy)
                    heroes_groups_list.append(heroes_groups)
            semaphores[thread_count].acquire()
            for original_hero_group, heroes_groups in zip(original_hero_group_list, heroes_groups_list):
                print(f'{bond}：{original_hero_group}\n'+''.join(heroes_groups))
        elif population > 0:
            function1 = hero_group_generate(population, bonds_group, hero_numbers, price_sum_max, values_list_best,values_list_rest_best)
            heroes_groups = function1['heroes_groups']
            semaphores[thread_count].acquire()
            print(f'{bond}：{original_hero_group}\n'+''.join(heroes_groups))
        else:
            semaphores[thread_count].acquire()
            print(f'{bond}：{original_hero_group}')
        try:
            semaphores[thread_count + 1].release()
        except:
            pass
    def hero_group_generate(population, bonds_group, hero_numbers, price_sum_max, values_list_best,values_list_rest_best, heroes_groups=[]):
        flag=False
        for a in range(len(names)):
            population_copy = population - sizes[a]
            result = [a]
            if not(a in hero_numbers or set(combined_heroes_index).issubset(set(result + hero_numbers))):
                if population_copy == 0:
                    function2 = match_machine(result, bonds_group, values_list_best, heroes_groups, price_sum_max,values_list_rest_best,flag)
                    values_list_best = function2['values_list_best']
                    values_list_rest_best = function2['values_list_rest_best']
                    heroes_groups = function2['heroes_groups']
                    price_sum_max = function2['price_sum_max']
                    flag=function2['flag']
                elif population_copy > 0:
                    for b in range(a + 1, len(names)):
                        population_copy = population - sizes[a] - sizes[b]
                        result = [a, b]
                        if not (b in hero_numbers or set(combined_heroes_index).issubset(set(result + hero_numbers))):
                            if population_copy == 0:
                                function2 = match_machine(result, bonds_group, values_list_best, heroes_groups,price_sum_max, values_list_rest_best,flag)
                                values_list_best = function2['values_list_best']
                                values_list_rest_best = function2['values_list_rest_best']
                                heroes_groups = function2['heroes_groups']
                                price_sum_max = function2['price_sum_max']
                                flag=function2['flag']
                            elif population_copy > 0:
                                for c in range(b + 1, len(names)):
                                    population_copy = population - sizes[a] - sizes[b] - sizes[c]
                                    result = [a, b, c]
                                    if not (c in hero_numbers or set(combined_heroes_index).issubset(set(result + hero_numbers))):
                                        if population_copy == 0:
                                            function2 = match_machine(result, bonds_group, values_list_best,heroes_groups, price_sum_max,values_list_rest_best,flag)
                                            values_list_best = function2['values_list_best']
                                            values_list_rest_best = function2['values_list_rest_best']
                                            heroes_groups = function2['heroes_groups']
                                            price_sum_max = function2['price_sum_max']
                                            flag=function2['flag']
                                        elif population_copy > 0:
                                            for d in range(c + 1, len(names)):
                                                population_copy = population - sizes[a] - sizes[b] - sizes[c] - sizes[d]
                                                result = [a, b, c, d]
                                                if not (d in hero_numbers or set(combined_heroes_index).issubset(set(result + hero_numbers))):
                                                    if population_copy == 0:
                                                        function2 = match_machine(result, bonds_group, values_list_best,heroes_groups, price_sum_max,values_list_rest_best,flag)
                                                        values_list_best = function2['values_list_best']
                                                        values_list_rest_best = function2['values_list_rest_best']
                                                        heroes_groups = function2['heroes_groups']
                                                        price_sum_max = function2['price_sum_max']
                                                        flag=function2['flag']
                                                    elif population_copy > 0:
                                                        for e in range(d + 1, len(names)):
                                                            population_copy = population - sizes[a] - sizes[b] - sizes[c] - sizes[d] - sizes[e]
                                                            result = [a, b, c, d, e]
                                                            if not (e in hero_numbers or set(combined_heroes_index).issubset(set(result + hero_numbers))):
                                                                if population_copy == 0:
                                                                    function2 = match_machine(result, bonds_group,values_list_best,heroes_groups,price_sum_max,values_list_rest_best,flag)
                                                                    values_list_best = function2['values_list_best']
                                                                    values_list_rest_best = function2['values_list_rest_best']
                                                                    heroes_groups = function2['heroes_groups']
                                                                    price_sum_max = function2['price_sum_max']
                                                                    flag=function2['flag']
                                                                elif population_copy > 0:
                                                                    for f in range(e + 1, len(names)):
                                                                        population_copy = population - sizes[a] - sizes[b] - sizes[c] - sizes[d] - sizes[e] - sizes[f]
                                                                        result = [a, b, c, d, e, f]
                                                                        if not (f in hero_numbers or set(combined_heroes_index).issubset(set(result + hero_numbers))):
                                                                            if population_copy == 0:
                                                                                function2 = match_machine(result,bonds_group,values_list_best,heroes_groups,price_sum_max,values_list_rest_best,flag)
                                                                                values_list_best = function2['values_list_best']
                                                                                values_list_rest_best = function2['values_list_rest_best']
                                                                                heroes_groups = function2['heroes_groups']
                                                                                price_sum_max = function2['price_sum_max']
                                                                                flag=function2['flag']
                                                                            elif population_copy > 0:
                                                                                for g in range(f + 1, len(names)):
                                                                                    population_copy = population -sizes[a] - sizes[b] - sizes[c] - sizes[d] - sizes[e] - sizes[f] - sizes[g]
                                                                                    result = [a, b, c, d, e, f, g]
                                                                                    if not (g in hero_numbers or set(combined_heroes_index).issubset(set(result + hero_numbers))):
                                                                                        if population_copy == 0:
                                                                                            function2 = match_machine(result, bonds_group,values_list_best,heroes_groups,price_sum_max,values_list_rest_best,flag)
                                                                                            values_list_best =function2['values_list_best']
                                                                                            values_list_rest_best =function2['values_list_rest_best']
                                                                                            heroes_groups = function2['heroes_groups']
                                                                                            price_sum_max = function2['price_sum_max']
                                                                                            flag=function2['flag']
                                                                                        elif population_copy > 0:
                                                                                            for h in range(g + 1,len(names)):
                                                                                                population_copy = population -sizes[a] -sizes[b] -sizes[c] -sizes[d] -sizes[e] -sizes[f] -sizes[g] -sizes[h]
                                                                                                result = [a, b, c, d, e,f, g, h]
                                                                                                if not (h in hero_numbers or set(combined_heroes_index).issubset(set(result + hero_numbers))):
                                                                                                    if population_copy == 0:
                                                                                                        function2 = match_machine(result,bonds_group,values_list_best,heroes_groups,price_sum_max,values_list_rest_best,flag)
                                                                                                        values_list_best =function2['values_list_best']
                                                                                                        values_list_rest_best =function2['values_list_rest_best']
                                                                                                        heroes_groups =function2['heroes_groups']
                                                                                                        price_sum_max =function2['price_sum_max']
                                                                                                        flag=function2['flag']
                                                                                                    elif population_copy > 0:
                                                                                                        for i in range(h + 1,len(names)):
                                                                                                            population_copy = population -sizes[a] -sizes[b] -sizes[c] -sizes[d] -sizes[e] -sizes[f] -sizes[g] -sizes[h] -sizes[i]
                                                                                                            result = [a,b,c,d,e,f,g,h,i]
                                                                                                            if not (i in hero_numbers or set(combined_heroes_index).issubset(set(result + hero_numbers))):
                                                                                                                if population_copy == 0:
                                                                                                                    function2 = match_machine(result,bonds_group,values_list_best,heroes_groups,price_sum_max,values_list_rest_best,flag)
                                                                                                                    values_list_best =function2['values_list_best']
                                                                                                                    values_list_rest_best =function2['values_list_rest_best']
                                                                                                                    heroes_groups =function2['heroes_groups']
                                                                                                                    price_sum_max =function2['price_sum_max']
                                                                                                                    flag=function2['flag']
                                                                                                                elif population_copy > 0:
                                                                                                                    for j in range(i + 1,len(names)):
                                                                                                                        population_copy = population -sizes[a] -sizes[b] -sizes[c] -sizes[d] -sizes[e] -sizes[f] -sizes[g] -sizes[h] -sizes[i] -sizes[j]
                                                                                                                        result = [a,b,c,d,e,f,g,h,i,j]
                                                                                                                        if not (j in hero_numbers or set(combined_heroes_index).issubset(set(result + hero_numbers))):
                                                                                                                            if population_copy == 0:
                                                                                                                                function2 = match_machine(result,bonds_group,values_list_best,heroes_groups,price_sum_max,values_list_rest_best,flag)
                                                                                                                                values_list_best =function2['values_list_best']
                                                                                                                                values_list_rest_best =function2['values_list_rest_best']
                                                                                                                                heroes_groups =function2['heroes_groups']
                                                                                                                                price_sum_max =function2['price_sum_max']
                                                                                                                                flag=function2['flag']
        return {'flag':flag,'heroes_groups': heroes_groups, 'price_sum_max': price_sum_max, 'values_list_best': values_list_best,'values_list_rest_best': values_list_rest_best}
    def match_machine(result, bonds_group, values_list_best, heroes_groups, price_sum_max, values_list_rest_best,flag):
        heroes_group = []
        price_sum = 0
        bonds_combos = copy.deepcopy(bonds_group)
        for e in result:
            heroes_group.insert(print_index_if_value_is_larger(heroes_group, prices[e]), f'{names[e]}({prices[e]})')
            price_sum += prices[e]
            for f in hero_bonds[e]:
                try:
                    bonds_combos[f] += 1
                except:
                    bonds_combos[f] = 1
        values_list = []
        values_list_rest = []
        for key, value in bonds_combos.items():
            value_result = 0
            value_plus_rest = 0
            match = bonds.index(key)
            for h in number_of_bonds[match]:
                if value >= h:
                    value_result = h
                    if value > h:
                        value_plus_rest = value
                    break
            if value_result > 0:
                values_list.append(value_result)
            if value_plus_rest > 0:
                values_list_rest.append(value_plus_rest)
        values_list.sort(reverse=True)
        values_list_rest.sort(reverse=True)
        if values_list > values_list_best:
            values_list_best = values_list
            values_list_rest_best = values_list_rest
            heroes_groups = [heroes_group]
            price_sum_max = price_sum
            flag=True
        elif values_list == values_list_best:
            if values_list_rest > values_list_rest_best:
                values_list_best = values_list
                values_list_rest_best = values_list_rest
                heroes_groups = [heroes_group]
                price_sum_max = price_sum
                flag=True
            elif values_list_rest == values_list_rest_best:
                if price_sum > price_sum_max:
                    values_list_best = values_list
                    values_list_rest_best = values_list_rest
                    heroes_groups = [heroes_group]
                    price_sum_max = price_sum
                    flag=True
                elif price_sum == price_sum_max:
                    heroes_groups.append(heroes_group)
        return {'values_list_best': values_list_best, 'heroes_groups': heroes_groups, 'price_sum_max': price_sum_max,'values_list_rest_best': values_list_rest_best,'flag':flag}
    async def main():
        async with aiohttp.ClientSession() as session:
            races_text=await fetch(session,'https://game.gtimg.cn/images/lol/act/img/tft/js/race.js')
            with Pool() as pool:
                result_first=pool.apply_async(bonds_deal,args=(races_text,))
                races, number_of_bonds_first = result_first.get()
        async with aiohttp.ClientSession() as session:
            jobs_text = await fetch(session, 'https://game.gtimg.cn/images/lol/act/img/tft/js/job.js')
            with Pool() as pool:
                result_second=pool.apply_async(bonds_deal,args=(jobs_text,))
                jobs,number_of_bonds_second=result_second.get()
        async with aiohttp.ClientSession() as session:
            chesses_text =await fetch(session, 'https://game.gtimg.cn/images/lol/act/img/tft/js/chess.js')
            with Pool() as pool:
                result_third=pool.apply_async(chesses_deal,args=(chesses_text,))
                names,hero_bonds,prices,sizes,combined_heroes_index=result_third.get()
        while not (races and jobs and names):
            pass
        return races+jobs,number_of_bonds_first+number_of_bonds_second,names,hero_bonds,prices,sizes,combined_heroes_index
    async def fetch(session,url):
        async with session.get(url) as response:
            return await response.text()
    result=asyncio.run(main())
    bonds,number_of_bonds,names,hero_bonds,prices,sizes,combined_heroes_index=result
    population=10
    semaphores=[Semaphore(0)]
    semaphores[0].release()
    thread_count=0
    threads=[]
    for i in range(len(number_of_bonds)):
        if number_of_bonds[i][0]>1:
            thread_count+=1
            bond=bonds[i]
            t = Thread(target=final_generate, args=(thread_count,bond,population))
            semaphores.append(Semaphore(0))
            t.start()
            threads.append(t)
    for t in threads:
        t.join()