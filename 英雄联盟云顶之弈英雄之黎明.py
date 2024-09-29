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
        if int(item['price']) > 0:
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
    return names,hero_bonds,prices,sizes
if __name__ == "__main__":
    from threading import Semaphore
    import copy,asyncio,aiohttp
    from multiprocessing import Pool
    from concurrent.futures import ThreadPoolExecutor
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
    def final_generate(thread_count, bond):
        bonds_group = {}
        original_hero_group = []
        values_list_best = []
        values_list_rest_best = []
        hero_numbers = []
        population = 10
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
        if population > 0:
            heroes_groups= hero_group_generate(population, bonds_group, hero_numbers, price_sum_max, values_list_best,values_list_rest_best)
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
        for a in range(len(names)):
            population_copy = population - sizes[a]
            result = [a]
            if a not in hero_numbers:
                if population_copy > 0:
                    for b in range(a + 1, len(names)):
                        population_copy = population - sizes[a] - sizes[b]
                        result = [a, b]
                        if b not in hero_numbers:
                            if population_copy > 0:
                                for c in range(b + 1, len(names)):
                                    population_copy = population - sizes[a] - sizes[b] - sizes[c]
                                    result = [a, b, c]
                                    if c not in hero_numbers:
                                        if population_copy > 0:
                                            for d in range(c + 1, len(names)):
                                                population_copy = population - sizes[a] - sizes[b] - sizes[c] - sizes[d]
                                                result = [a, b, c, d]
                                                if d not in hero_numbers:
                                                    if population_copy > 0:
                                                        for e in range(d + 1, len(names)):
                                                            population_copy = population - sizes[a] - sizes[b] - sizes[c] - sizes[d] - sizes[e]
                                                            result = [a, b, c, d, e]
                                                            if e not in hero_numbers:
                                                                if population_copy > 0:
                                                                    for f in range(e + 1, len(names)):
                                                                        population_copy = population - sizes[a] - sizes[b] - sizes[c] - sizes[d] - sizes[e] - sizes[f]
                                                                        result = [a, b, c, d, e, f]
                                                                        if f not in hero_numbers:
                                                                            if population_copy > 0:
                                                                                for g in range(f + 1, len(names)):
                                                                                    population_copy = population - sizes[a] - sizes[b] - sizes[c] - sizes[d] - sizes[e] - sizes[f] - sizes[g]
                                                                                    result = [a, b, c, d, e, f, g]
                                                                                    if g not in hero_numbers:
                                                                                        if population_copy > 0:
                                                                                            for h in range(g + 1, len(names)):
                                                                                                population_copy = population - sizes[a] - sizes[b] - sizes[c] - sizes[d] - sizes[e] - sizes[f] - sizes[g] - sizes[h]
                                                                                                result = [a, b, c, d, e, f, g, h]
                                                                                                if h not in hero_numbers:
                                                                                                    if population_copy > 0:
                                                                                                        for i in range(h + 1, len(names)):
                                                                                                            population_copy = population - sizes[a] - sizes[b] - sizes[c] - sizes[d] - sizes[e] - sizes[f] - sizes[g] - sizes[h] - sizes[i]
                                                                                                            result = [a, b, c, d, e, f, g, h, i]
                                                                                                            if i not in hero_numbers:
                                                                                                                if population_copy > 0:
                                                                                                                    for j in range(i + 1, len(names)):
                                                                                                                        population_copy = population - sizes[a] - sizes[b] - sizes[c] - sizes[d] - sizes[e] - sizes[f] - sizes[g] - sizes[h] - sizes[i] - sizes[j]
                                                                                                                        result = [a, b, c, d, e, f, g, h, i, j]
                                                                                                                        if j not in hero_numbers:
                                                                                                                            if population_copy==0:
                                                                                                                                values_list_rest,heroes_groups,price_sum_max,values_list_rest_best=match_machine(result, bonds_group, values_list_best, heroes_groups, price_sum_max,values_list_rest_best)
                                                                                                                elif population_copy==0:
                                                                                                                    values_list_rest,heroes_groups,price_sum_max,values_list_rest_best=match_machine(result, bonds_group, values_list_best, heroes_groups, price_sum_max,values_list_rest_best)
                                                                                                    elif population_copy==0:
                                                                                                        values_list_rest,heroes_groups,price_sum_max,values_list_rest_best=match_machine(result, bonds_group, values_list_best, heroes_groups, price_sum_max,values_list_rest_best)
                                                                                        elif population_copy==0:
                                                                                            values_list_rest,heroes_groups,price_sum_max,values_list_rest_best=match_machine(result, bonds_group, values_list_best, heroes_groups, price_sum_max,values_list_rest_best)
                                                                            elif population_copy==0:
                                                                                values_list_rest,heroes_groups,price_sum_max,values_list_rest_best=match_machine(result, bonds_group, values_list_best, heroes_groups, price_sum_max,values_list_rest_best)
                                                                elif population_copy==0:
                                                                    values_list_rest,heroes_groups,price_sum_max,values_list_rest_best=match_machine(result, bonds_group, values_list_best, heroes_groups, price_sum_max,values_list_rest_best)
                                                    elif population_copy==0:
                                                        values_list_rest,heroes_groups,price_sum_max,values_list_rest_best=match_machine(result, bonds_group, values_list_best, heroes_groups, price_sum_max,values_list_rest_best)
                                        elif population_copy==0:
                                            values_list_rest,heroes_groups,price_sum_max,values_list_rest_best=match_machine(result, bonds_group, values_list_best, heroes_groups, price_sum_max,values_list_rest_best)
                            elif population_copy==0:
                                values_list_rest,heroes_groups,price_sum_max,values_list_rest_best=match_machine(result, bonds_group, values_list_best, heroes_groups, price_sum_max,values_list_rest_best)
                elif population_copy==0:
                    values_list_rest,heroes_groups,price_sum_max,values_list_rest_best=match_machine(result, bonds_group, values_list_best, heroes_groups, price_sum_max,values_list_rest_best)
        return heroes_groups
    def match_machine(result, bonds_group, values_list_best, heroes_groups, price_sum_max, values_list_rest_best):
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
        elif values_list == values_list_best:
            if values_list_rest > values_list_rest_best:
                values_list_best = values_list
                values_list_rest_best = values_list_rest
                heroes_groups = [heroes_group]
                price_sum_max = price_sum
            elif values_list_rest == values_list_rest_best:
                if price_sum > price_sum_max:
                    values_list_best = values_list
                    values_list_rest_best = values_list_rest
                    heroes_groups = [heroes_group]
                    price_sum_max = price_sum
                elif price_sum == price_sum_max:
                    heroes_groups.append(heroes_group)
        return values_list_rest,heroes_groups,price_sum_max,values_list_rest_best
    async def main():
        async with aiohttp.ClientSession() as session:
            races_text=await fetch(session,'https://game.gtimg.cn/images/lol/act/img/tft/js/14.19-2024.S12-2/race-2.js')
            with Pool() as pool:
                result_first=pool.apply_async(bonds_deal,args=(races_text,))
                races, number_of_bonds_first = result_first.get()
        async with aiohttp.ClientSession() as session:
            jobs_text = await fetch(session, 'https://game.gtimg.cn/images/lol/act/img/tft/js/14.19-2024.S12-2/job-2.js')
            with Pool() as pool:
                result_second=pool.apply_async(bonds_deal,args=(jobs_text,))
                jobs,number_of_bonds_second=result_second.get()
        async with aiohttp.ClientSession() as session:
            chesses_text =await fetch(session, 'https://game.gtimg.cn/images/lol/act/img/tft/js/14.19-2024.S12-2/chess-2.js')
            with Pool() as pool:
                result_third=pool.apply_async(chesses_deal,args=(chesses_text,))
                names,hero_bonds,prices,sizes=result_third.get()
        while not(races and jobs and names):
            pass
        return races+jobs,number_of_bonds_first+number_of_bonds_second,names,hero_bonds,prices,sizes
    async def fetch(session,url):
        async with session.get(url) as response:
            return await response.text()
    result=asyncio.run(main())
    with ThreadPoolExecutor() as executor:
        bonds, number_of_bonds, names, hero_bonds, prices, sizes = result
        semaphores = [Semaphore(0)]
        semaphores[0].release()
        thread_count = 0
        for i in range(len(number_of_bonds)):
            if number_of_bonds[i][0]>1:
                bond = bonds[i]
                if thread_count>0:
                    executor.submit(final_generate, thread_count, bond)
                    semaphores.append(Semaphore(0))
                else:
                    executor.submit(final_generate, thread_count, bond)
                thread_count+=1