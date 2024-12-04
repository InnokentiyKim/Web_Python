


adv_view = AdvView.as_view("advs")
user_view = UserView.as_view("users")
advs_list_view = AdvListView.as_view("advs_list")

app.add_url_rule(rule="/api/adv", view_func=advs_list_view, methods=['GET'])

app.add_url_rule(rule="/api/adv/<int:adv_id>", view_func=adv_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule(rule="/api/adv", view_func=adv_view, methods=['POST'])

app.add_url_rule(rule="/api/user/<int:user_id>", view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule(rule="/api/user", view_func=user_view, methods=['POST'])