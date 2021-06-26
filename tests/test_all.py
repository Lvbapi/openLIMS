from urllib.request import urlopen

import flask_login as login
import pytest
from flask import url_for
from flask_login import LoginManager

import src as my_app
from src.auth.models import Role, User
from src.helpers.utils import slugify
from src.site.models import Page, Post


@pytest.fixture
def app():
    login_manager = LoginManager()
    login_manager.init_app(my_app.application)

    app = my_app.application

    @login_manager.user_loader
    def load_user(user_id):
        return User().get_by_id(user_id)

    return app


@pytest.fixture
def session():
    return my_app.db.session


########################
### Live server tests ##
########################
@pytest.mark.usefixtures('live_server')
class TestLiveServer:

    def test_serve_site_index(self):
        res = urlopen(url_for('site.index', _external=True))
        assert res.code == 200

    def test_serve_site_blog(self):
        res = urlopen(url_for('site.blog', _external=True))
        assert b'Blog' in res.read()
        assert res.code == 200

    def test_serve_site_about(self):
        res = urlopen(url_for('site.site_page', page='about', _external=True))
        assert b'About' in res.read()
        assert res.code == 200


#################
### Utils Test ##
#################
def test_slugify(client):
    expected = 'test-this'
    assert slugify('test this') == expected


#######################
### ADMIN Login Test ##
#######################
def test_login(client):
    credentials = {'email': 'admin@example.com', 'password': 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'


#########################
### ADMIN Edit Profile ##
#########################
def test_admin_edit_profile(client):
    credentials = {'email': 'admin@example.com', 'password': 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    res = client.get(url_for('admin.edit_profile'))
    assert res.status_code == 200
    client.post(url_for('admin.edit_profile'), data={'first_name':'test', 'email':'admin@example.com', 'password':'admin', 'alias':'Admin'})
    assert login.current_user.first_name == 'test'


#################
### ADMIN BLOG ##
#################
def test_admin_blog_list(client):
    credentials = {'email': 'admin@example.com', 'password': 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    res = client.get(url_for('admin.blog_list'))
    assert res.status_code == 200


def test_admin_blog_post_create(live_server, client):
    credentials = {'email' : 'admin@example.com', 'password' : 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    post = {'title' : 'blog create test', 'text' : 'testing blog post','published' : '1'}
    client.post(url_for('admin.create_post'), data=post)
    res = urlopen(url_for('site.single_post', slug='blog-create-test', _external=True))
    assert res.code == 200
    assert b'testing' in res.read()


def test_admin_blog_post_edit(live_server, client):
    credentials = {'email' : 'admin@example.com', 'password' : 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    pid = Post.get_by_slug('blog-create-test').get_id()
    post = {'id' : pid, 'title' : 'blog create test', 'text' : 'updated testing blog post','published' : '1'}
    client.post(url_for('admin.edit_post', post_id=pid), data=post)
    res = urlopen(url_for('site.single_post', slug='blog-create-test', _external=True))
    assert res.code == 200
    assert b'updated' in res.read()


def test_admin_blog_post_delete(live_server, client):
    credentials = {'email': 'admin@example.com', 'password': 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    post = Post.get_by_slug('blog-create-test').get_id()
    client.get(url_for('admin.delete_post', post_id=post))
    res = client.get(url_for('site.single_post', slug='blog-create-test'))
    assert res.status_code == 404


#####################
### ADMIN Comments ##
#####################
def test_admin_comments_list(client):
    credentials = {'email': 'admin@example.com', 'password': 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    res = client.get(url_for('admin.comment_list'))
    assert res.status_code == 200


def test_admin_comment_create(live_server, client):
    credentials = {'email' : 'admin@example.com', 'password' : 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    post = Post.get_by_id(1)
    comment = {'written_by' : '1', 'post' : post.get_id(), 'comment' : 'testing comment','published' : '1'}
    client.post(url_for('admin.create_comment'), data=comment)
    res = urlopen(url_for('site.single_post', slug=post.get_slug(), _external=True))
    assert res.code == 200
    assert b'testing comment' in res.read()


def test_admin_comment_edit(live_server, client):
    credentials = {'email' : 'admin@example.com', 'password' : 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    post = Post.get_by_id(1)
    cid = post.comments[-1].get_id()
    comment = {'id' : cid, 'written_by' : '1', 'post' : post.get_id(), 'comment' : 'updated testing comment','published' : '1'}
    client.post(url_for('admin.edit_comment', comment_id=cid), data=comment)
    res = urlopen(url_for('site.single_post', slug=post.get_slug(), _external=True))
    assert res.code == 200
    assert b'updated testing comment' in res.read()


def test_admin_comment_delete(live_server, client):
    credentials = {'email': 'admin@example.com', 'password': 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    post = Post.get_by_id(1)
    cid = post.comments[-1].get_id()
    client.get(url_for('admin.delete_comment', comment_id=cid))
    res = urlopen(url_for('site.single_post', slug=post.get_slug(), _external=True))
    assert res.code == 200
    assert b'updated testing comment' not in res.read()


##################
### ADMIN Pages ##
##################
def test_admin_pages_list(client):
    credentials = {'email': 'admin@example.com', 'password': 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    res = client.get(url_for('admin.page_list'))
    assert res.status_code == 200
    res = client.get(url_for('admin.page_list', page=2))
    assert res.status_code == 200

def test_admin_page_create(live_server, client):
    credentials = {'email' : 'admin@example.com', 'password' : 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    page = {'title' : 'test page', 'html' : 'testing page','published' : '1'}
    client.post(url_for('admin.create_page'), data=page)
    res = urlopen(url_for('site.site_page', page='test-page', _external=True))
    assert res.code == 200
    assert b'testing' in res.read()


def test_admin_page_edit(live_server, client):
    credentials = {'email' : 'admin@example.com', 'password' : 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    pid = Page.get_by_slug('test-page').get_id()
    page = {'id' : pid, 'title': 'test page', 'html': 'updated testing page', 'published': '1'}
    client.post(url_for('admin.edit_page', page_id=pid), data=page)
    res = urlopen(url_for('site.site_page', page='test-page', _external=True))
    assert res.code == 200
    assert b'updated' in res.read()


def test_admin_page_delete(live_server, client):
    credentials = {'email': 'admin@example.com', 'password': 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    pid = Page.get_by_slug('test-page').get_id()
    client.get(url_for('admin.delete_page', page_id=pid))
    res = client.get(url_for('site.site_page', page='test-page'))
    assert res.status_code == 404


##################
### ADMIN Roles ##
##################
def test_admin_roles_list(client):
    credentials = {'email': 'admin@example.com', 'password': 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    res = client.get(url_for('admin.role_list'))
    assert res.status_code == 200


##################
### ADMIN Users ##
##################
def test_admin_users_list(client):
    credentials = {'email': 'admin@example.com', 'password': 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    res = client.get(url_for('admin.user_list'))
    assert res.status_code == 200


##########################
### ADMIN Site Settings ##
##########################
def test_admin_site_settings(client):
    credentials = {'email': 'admin@example.com', 'password': 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    res = client.get(url_for('admin.site_settings'))
    assert res.status_code == 200


####################
### AUTH Register ##
####################
def test_registration(client):
    credentials = {'email': 'test@example.com', 'password': 'test'}
    client.post(url_for('auth.registration_view'), data=credentials)
    assert login.current_user.email == 'test@example.com'


##########################################################
### AUTH Register - default registration gives no roles ##
##########################################################
def test_newly_registered_user_has_no_roles(client):
    user = User().get_user_by_email('test@example.com')
    roles = user.get_roles()
    assert roles == []


##################
### AUTH Logout ##
##################
def test_logout(client):
    credentials = {'email': 'admin@example.com', 'password': 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    client.get(url_for('auth.logout_view'))
    assert login.current_user.is_anonymous


#################
### AUTH Login ##
#################


###################################
### Delete newly registered user ##
###################################
def test_delete_newly_registered_user(session):
    user = User().get_user_by_email('test@example.com')
    session.delete(user)
    session.commit()
    assert User().get_user_by_email('test@example.com') == None


############################
### current_user is_admin ##
############################
def test_admin_is_admin(client):
    credentials = {'email': 'admin@example.com', 'password': 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    assert login.current_user.is_admin


######################
### 3 default roles ##
######################
def test_there_are_three_roles(client):
    roles = Role().all()
    assert len(roles) == 3


##############################
### admin has default roles ##
##############################
def test_admin_has_all_roles(client):
    credentials = {'email': 'admin@example.com', 'password': 'admin'}
    client.post(url_for('auth.login_view'), data=credentials)
    assert login.current_user.email == 'admin@example.com'
    roles = Role().all()
    for role in roles:
        assert login.current_user.has_role(role)


######################
### 404 errors work ##
######################
def test_post_404(client):
    assert client.get(url_for('site.single_post', slug='test')).status_code == 404


def test_page_404(client):
    assert client.get(url_for('site.site_page', page='test')).status_code == 404


###########################################
### default site index redirects to blog ##
###########################################
def test_site_index_redirect(client):
    assert client.get(url_for('site.index')).status_code == 302


####################
### User add user ##
####################
def test_add_user(session):
    user = User()
    user.email = 'test@example.com'
    session.add(user)
    session.flush()
    uid = user.id
    session.commit()
    assert uid == User().get_user_by_email('test@example.com').id


######################
### User login user ##
######################
def test_login_user(client):
    user = User().get_user_by_email('test@example.com')
    login.login_user(user)
    assert login.current_user.email == user.email


#######################
### User delete user ##
#######################
def test_delete_user(session):
    user = User().get_user_by_email('test@example.com')
    session.delete(user)
    session.commit()
    assert User().get_user_by_email('test@example.com') == None


#############################
### Test Home Page is blog ##
#############################
def test_home_page(live_server, client):
    res = urlopen(url_for('site.index', _external=True))
    assert res.code == 200
    assert b'Long Hello' in res.read()


###############
### Test 405 ##
###############
def test_render_405(client):
    assert client.put(url_for('site.site_page', page='test'), data={}).status_code == 405
