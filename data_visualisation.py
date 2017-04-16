import matplotlib.pyplot as plt
from matplotlib import style
from vk_api import get_post_ids,count_comments


style.use('ggplot')
x_coords = []
y_coords = []

posts = get_post_ids()
for key in posts.keys():
    x_coords.append(key)
    sum = 0
    for elem in posts[key]:
        sum+=int(count_comments(elem))
    y_coords.append(sum)
# plt.plot(x_coords,y_coords)
# plt.scatter(x_coords,y_coords)
# plt.scatter(x_coords, y_coords, c='red', marker='^', s=60)
plt.bar(range(len(x_coords)),y_coords)
plt.title('Graph')
plt.xlabel('x')
plt.xticks(range(len(x_coords)),x_coords)
plt.ylabel('y')
new_y_coords = [60,80,70,90]
plt.show()
# plt.savefig('pics/sample_plot.png', format='png')
