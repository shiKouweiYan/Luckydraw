import random
import time
import os
# 新建空字典，维护当前的用户id和积分
curpointdict = {}
with open('updates.csv','w'):
    pass
print('积分变动：')
while True:
    time.sleep(random.randrange(60, 1200))  # 睡眠从60到1200秒的一段时间
    if time.strftime("%w", time.localtime()) == '6' and int(time.strftime("%H", time.localtime())) >= 23:
        # 如果超出了周六晚上23点，就退出循环开始抽奖。
        break
    id = random.randint(0, 10)  # 在指定范围内随机生成ID
    point = random.randrange(-1000, 1000)  # 在（-1000，+1000）范围内生成积分变动
    if id in curpointdict.keys():
        if curpointdict[id] + point >= 0:  # 判断积分变动是否有效
            # 维护字典
            curpointdict[id] = curpointdict[id] + point
            # 在csv文件中记录积分变动
            with open('updates.csv', 'a') as updates:
                updates.write('%d,%+d\n' % (id, point))
            # end with
            print('%d '%id, '%+d'%point)
    else:  # 即如果id不在字典里
        if point > 0:
            # 维护字典，新建键值为id的项
            curpointdict[id] = point
            # 在csv文件中记录积分变动
            with open('updates.csv', 'a') as updates:
                updates.write('%d,%+d\n' % (id, point))
            # end with
            print('%d '% id, '%+d'% point)  # 打印积分变动

# 进入抽奖环节
lines = ['%d,%d\n' % (k, v) for k, v in curpointdict.items()]  # 从字典中读取当前用户积分
with open('Candidate.csv', 'w') as f:
    f.writelines(lines)
# 将当前用户积分写入Candidate.csv
print('当前用户积分：')
with open('Candidate.csv', 'r') as f:
    for line in f:
        print(line.replace(',', ':'), end='')
print()
# 在屏幕上显示当前用户积分
candidate_dict = curpointdict
def choujiang():
    '''用来每轮抽一等奖、二等奖'''
    # 开始抽一等奖
    prize_one_dict = {}  # 新建一等奖候选人字典
    for k in candidate_dict.keys():
        if candidate_dict[k] >= 1000:
            prize_one_dict[k] = candidate_dict[k]  # 将候选人字典中符合要求：积分大等于1000者加入字典。
    if prize_one_dict:  # 如果字典为空则无人符合一等奖条件，一等奖空缺。
        prize_one_can = list(prize_one_dict.keys())  # 一等奖候选人id列表
        weightlist = [int(str(prize_one_dict[id])[:1]) for id in prize_one_can]
        # 设置权重列表，权重恰好是当前积分的首位。列表推导：获取键值id对应的积分后转化为字符串取首位切片，再转化为整数。
        prizeone = random.choices(prize_one_can, weights=weightlist)
        # 使用random.choices(population,weights = [])为prize_one_can设置权重,开始抽奖
        print ('%d 一等奖'%prizeone[0])
        del candidate_dict[prizeone[0]] # 在候选人名单字典中删除获奖者
    # 抽二等奖
    prizetwolist = []  # 新建二等奖候选人列表
    for k in candidate_dict.keys():
        if candidate_dict[k] > 0:
            prizetwolist.append(k)  # 将符合要求：积分大于0者加入列表。
    # 抽两个二等奖
    for i in range(2):
        if prizetwolist:  # 检验二等奖名单里面是否还有人
            prizetwo = random.choice(prizetwolist)  # 从二等奖候选人名单里随机一个二等奖
            print('%d 二等奖' % prizetwo)
            del candidate_dict[prizetwo]  # 从总候选人字典里删掉中奖者
            prizetwolist.remove(prizetwo)  # 从二等奖候选人名单里删掉中奖者


print('抽奖开始：')
if candidate_dict:  # 如果候选人名单为空，则不抽奖。
    print('第1轮：')
    choujiang()
for i in range(2, 4):
    if candidate_dict:  # 如果候选人名单为空，则直接结束。
        time.sleep(20*60)  # 睡20分钟
        print('第%d轮：' % i)
        choujiang()
    else:
        break
print('本周抽奖结束')

today = time.strftime("%Y-%m-%d", time.localtime())
os.rename('updates.csv', '%s.csv' % today)  # 将文件名改为今天的日期
# 程序结束