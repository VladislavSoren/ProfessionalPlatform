from my_projects.config import file_description_list, file_description_list_koncert_bot


def get_template_names_dict(description_dir):
    template_names_dict = {}
    for filename, template_name in file_description_list:
        description_path = description_dir / filename
        with open(description_path, mode='r') as f:
            template_names_dict[template_name] = f.readlines()

    return template_names_dict


def get_template_names_koncert_bot_dict(description_dir):
    template_names_dict = {}
    for filename, template_name in file_description_list_koncert_bot:
        description_path = description_dir / filename
        with open(description_path, mode='r') as f:

            if filename == 'platforms.txt':
                platforms_paras = f.readlines()
                platforms_names = platforms_paras[0:3]
                platforms_urls = platforms_paras[3:]
                platforms_names_urls_zip = zip(platforms_names, platforms_urls)
                template_names_dict[template_name] = platforms_names_urls_zip
            else:
                template_names_dict[template_name] = f.readlines()

    return template_names_dict
