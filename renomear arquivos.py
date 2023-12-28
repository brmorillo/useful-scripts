import os

def rename_files(base_folder, serie_name):
    season_counter = 1
    for season_folder in sorted(os.listdir(base_folder)):
        season_path = os.path.join(base_folder, season_folder)

        # Renomear a pasta da temporada
        new_season_name = f"Season {season_counter:02}"
        new_season_path = os.path.join(base_folder, new_season_name)
        os.rename(season_path, new_season_path)

        episode_counter = 1
        for episode_file in sorted(os.listdir(new_season_path)):
            episode_path = os.path.join(new_season_path, episode_file)

            # Manter a extensão do arquivo
            file_extension = os.path.splitext(episode_file)[1]

            # Renomear o arquivo do episódio
            new_episode_name = f"{serie_name} S{season_counter:02}E{episode_counter:02}{file_extension}"
            new_episode_path = os.path.join(new_season_path, new_episode_name)

            os.rename(episode_path, new_episode_path)
            episode_counter += 1

        season_counter += 1

# Modificar essas variáveis de acordo com o seu caso

base_folder = "C:\\Users\\bruno\\Downloads\\20 Years Old Beyond the Line"
serie_name = "20 Years Old Beyond the Line"

rename_files(base_folder, serie_name)
