# Hacker News
A scrapper of https://news.ycombinator.com site

**Special Note: If you don't have docker**

- Create a docker id.
- Open [Docker Sandbox Environment](https://labs.play-with-docker.com) and create a session there
- Create a new instance. Docker and git will already be installed there.
- Run the below mentioned commands

## Preinstall Requisites

- `docker==18.09.0`
- `docker-compose==1.23.2`

### Note

- Run `usermod -aG docker $USER`
- Reboot system to avoid using sudo every time when you run docker.

## Installation

Note: This deployment scripts expects `docker` command to be run without using `sudo` or `superuser mode`

### Production

```bash
git clone git://github.com/theBuzzyCoder/HackerNews.git HackerNews
cd HackerNews
bash ./system_setup/deploy-app
```

### Development Mode

```bash
git clone git://github.com/theBuzzyCoder/HackerNews.git HackerNews
cd HackerNews
bash ./system_setup/deploy-dev-mode
```

### Using Admin panel

Post Installation

```bash
docker container exec -it app python manage.py createsuperuser
```

Output

```
Username (leave blank to use 'root'):<your-username>
Email address:<your-email>
Password:<hidden>
Password (again):<hidden>
Superuser created successfully.
```

Now, load http://localhost/admin

### Running the downloader

```bash
docker container exec app python ../backend/htmlDownloader.py
```

- `--paginations` option is for number of pages to download. It's optional. By default, it's 3.

### Running the parser

```bash
docker container exec app python ../backend/htmlParser.py --extractor_model_id=1
```

- `--extractor_model_id` is mandatory argument to parse. It's the `id` field of post_extractor table

### Loading PHP-My-Admin

You can load phpmyadmin using this link: http://localhost:8080

For Login:
- Server: db
- User: admin
- Password: admin

## Roadmap

### Achieved Milestone

- [x] HTML Downloader
- [x] Downloaded HTML Parser
- [x] Post Django model
- [x] List View to view the post
- [x] Detail View to view the post
- [x] Ability to delete post for user
- [x] Ability to display new posts as new and read post as not new
- [x] Need to write installer to setup database
- [x] Ability to view downloaded HTML files
- [x] Ability to store path of downloaded HTML files in database.
- [x] Ability to pick stored HTML file from the file path

### Upcoming Milestone

- [ ] User Model for users to access post
- [ ] Ability for user to login to portal
- [ ] Ability to create account
- [ ] Ability to reset password
- [ ] Ability to automate the news updating on button click
