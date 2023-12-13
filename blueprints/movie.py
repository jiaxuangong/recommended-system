from flask import Blueprint, render_template, request, jsonify, g
import os
import random
from exts import db
from models import MovieModel, UserModel
from sqlalchemy import text, func
from actor import Actor
from critic import Critic
from state_repr import State_Repr
import torch
from agent import Agent
import torch as nn

bp = Blueprint("movie", __name__, url_prefix="/")

PER_PAGE = 6

# http://127.0.0.1:5000
# 在视图函数中处理分页逻辑
# 在视图函数中处理分页逻辑

recommended_movies_dict = {
    'user_id': None,  # 你需要在合适的地方设置实际的用户ID
    'recommended_movies': set()
}


@bp.route("/")
def index():
    results = []
    # if not g.user.viewed_movies:
    #     length=0
    # else:
    #     length=len(g.user.viewed_movies)
    if g.user and g.user.viewed_movies:
        # 用户已登录且有浏览历史
        user_id = g.user.id

        viewed_movies = g.user.viewed_movies
        # 假设 viewed_movies 是一个包含数字的字符串，如 "126090_182727_63131_6890_55253_31923"
        viewed_movies_str = g.user.viewed_movies
        # 用 "_" 符号分割字符串，得到字符串列表
        viewed_movies_list_str = viewed_movies_str.split("_")
        # 将字符串列表转换为整数列表
        viewed_movies_list_int = [int(movie_id) for movie_id in viewed_movies_list_str]
        length = len(viewed_movies_list_int)
        if length >= 5:

            # 获取用户的 ID
            user_id = g.user.id

            recommended_movies_dict['user_id'] = user_id

            limited_records = MovieModel.query.filter(MovieModel.id <= 3952).all()
            all_ids = [row.id for row in limited_records if row.id not in recommended_movies_dict['recommended_movies']]

            liked_items = viewed_movies_list_int[-5:]

            # 创建一个字典，将用户 ID 映射到整数列表
            user_viewed_movies = {'user_id': user_id, 'liked_items': liked_items, 'action_space': all_ids}

            # print(viewed_movies_list_int)
            # print(user_id)
            actor_path = 'S:/pythonProject/TextProject/model/actor.pth'
            critic_path = 'S:/pythonProject/TextProject/model/critic.pth'
            state_repr_path = 'S:/pythonProject/TextProject/model/state_repr.pth'
            agent = Agent()  # 创建 Agent 对象
            agent.load_model(actor_path, critic_path, state_repr_path)  # 调用 load_model 方法
            action_embed, items = agent.get_action(
                user_viewed_movies['user_id'],
                user_viewed_movies['liked_items'],
                user_viewed_movies['action_space'],
                False,
                9
            )

            recommandlist = items.tolist()
            print(recommandlist)
            # 执行处理浏览历史的逻辑，例如提取用户的浏览历史电影信息等
            # 这部分逻辑可以根据你的需求进行定制
            for i in recommandlist:
                # 添加已推荐的电影到集合中
                recommended_movies_dict['recommended_movies'].add(i)

                query = text("SELECT id, name, genre, intro,url FROM movie_infor WHERE id = :id")
                result = db.session.execute(query, {"id": i})
                for row in result:
                    movie_data = {'id': row.id, 'name': row.name, 'genre': row.genre, 'intro': row.intro,
                                  'url': row.url}
                results.append(movie_data)

            # results 中包含了六个不同的查询结果
            # 从每个结果列表中的第一个字典元素中提取 id 并创建一个新的列表
            id_list = [result['id'] for result in results]
            # id_list 中包含了每个结果列表中第一个字典元素的 id
            photo_folder = "static/movie_images"
            # 创建一个空列表来存储所有的文件名
            photo_list = []

            # 循环遍历 id_list，为每个 ID 生成文件名并检查文件是否存在
            for movie_id in id_list:
                photo_filename = f"{movie_id}.jpg"
                photo_path = os.path.join(photo_folder, photo_filename)
                if os.path.exists(photo_path):
                    photo_list.append(photo_path)

                # 现在，photo_list 包含了所有电影 ID 对应的存在的文件名
            return render_template('index.html', photos=photo_list, movie_infor=results)
        else:
            limited_records = MovieModel.query.filter(MovieModel.id <= 3952).all()
            all_ids = [row.id for row in limited_records]
            for _ in range(9):
                # 从容器中随机选择一个ID
                random_id = random.choice(all_ids)

                # 使用选定的ID执行查询
                query = text("SELECT id, name, genre, intro,url FROM movie_infor WHERE id = :id")
                result = db.session.execute(query, {"id": random_id})
                for row in result:
                    movie_data = {'id': row.id, 'name': row.name, 'genre': row.genre, 'intro': row.intro,
                                  'url': row.url}
                results.append(movie_data)

            # results 中包含了六个不同的查询结果
            # 从每个结果列表中的第一个字典元素中提取 id 并创建一个新的列表
            id_list = [result['id'] for result in results]
            # id_list 中包含了每个结果列表中第一个字典元素的 id
            photo_folder = "static/movie_images"
            # 创建一个空列表来存储所有的文件名
            photo_list = []

            # 循环遍历 id_list，为每个 ID 生成文件名并检查文件是否存在
            for movie_id in id_list:
                photo_filename = f"{movie_id}.jpg"
                photo_path = os.path.join(photo_folder, photo_filename)
                if os.path.exists(photo_path):
                    photo_list.append(photo_path)

                # 现在，photo_list 包含了所有电影 ID 对应的存在的文件名
            return render_template('index.html', photos=photo_list, movie_infor=results)




    else:
        limited_records = MovieModel.query.filter(MovieModel.id <= 3952).all()
        all_ids = [row.id for row in limited_records]
        for _ in range(9):
            # 从容器中随机选择一个ID
            random_id = random.choice(all_ids)

            # 使用选定的ID执行查询
            query = text("SELECT id, name, genre, intro,url FROM movie_infor WHERE id = :id")
            result = db.session.execute(query, {"id": random_id})
            for row in result:
                movie_data = {'id': row.id, 'name': row.name, 'genre': row.genre, 'intro': row.intro, 'url': row.url}
            results.append(movie_data)

        # results 中包含了六个不同的查询结果
        # 从每个结果列表中的第一个字典元素中提取 id 并创建一个新的列表
        id_list = [result['id'] for result in results]
        # id_list 中包含了每个结果列表中第一个字典元素的 id
        photo_folder = "static/movie_images"
        # 创建一个空列表来存储所有的文件名
        photo_list = []

        # 循环遍历 id_list，为每个 ID 生成文件名并检查文件是否存在
        for movie_id in id_list:
            photo_filename = f"{movie_id}.jpg"
            photo_path = os.path.join(photo_folder, photo_filename)
            if os.path.exists(photo_path):
                photo_list.append(photo_path)

            # 现在，photo_list 包含了所有电影 ID 对应的存在的文件名
        return render_template('index.html', photos=photo_list, movie_infor=results)


@bp.route('/save_history', methods=['GET'])
def save_history():
    movieID = request.args.get('movieID')

    if g.user:
        # 获取当前用户对象
        user = g.user

        # 获取当前用户的已浏览电影列表
        viewed_movies = user.viewed_movies

        if viewed_movies is None:
            # 如果viewed_movies为空，创建一个包含新电影ID的JSON数组
            viewed_movies = movieID
        else:
            # 如果不为空，将新电影ID添加到现有的JSON数组中，并只保留最后的十条电影id
            viewed_movies += '_' + movieID
            viewed_movies_list = viewed_movies.split('_')
            if len(viewed_movies_list) > 10:
                viewed_movies_list = viewed_movies_list[-10:]
            viewed_movies = '_'.join(viewed_movies_list)

        print(f"Updated viewed_movies: {viewed_movies}")  # 添加这一行

        # 更新数据库中的已浏览电影列表
        user.viewed_movies = viewed_movies
        db.session.commit()
        print("History updated successfully")  # 添加这一行

        return jsonify({'message': 'History updated successfully'})
    else:
        print('not log in')
        return jsonify({'message': 'User not logged in'})
