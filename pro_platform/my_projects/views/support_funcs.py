def get_template_names_dict(description_dir):
    file_description_list = [
        ('general_description.txt', 'general_description_paras'),
        ('service_functionality.txt', 'service_functionality_paras'),
        ('architecture.txt', 'architecture_paras'),
        ('project_implementation.txt', 'project_implementation_paras'),
        ('api_description.txt', 'api_description_paras'),
        ('links_to_source_code.txt', 'links_to_source'),
    ]

    template_names_dict = {}
    for filename, template_name in file_description_list:
        description_path = description_dir / filename
        with open(description_path, mode='r') as f:
            template_names_dict[template_name] = f.readlines()

    return template_names_dict


def get_template_names_koncert_bot_dict(description_dir):
    file_description_list = [
        ('general_description.txt', 'general_description_paras'),
        ('service_functionality.txt', 'service_functionality_paras'),
        ('platforms.txt', 'platforms_names_urls_zip'),
        ('architecture.txt', 'architecture_paras'),
        ('project_implementation.txt', 'project_implementation_paras'),
        ('service_url.txt', 'service_url'),
    ]

    template_names_dict = {}
    for filename, template_name in file_description_list:
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
