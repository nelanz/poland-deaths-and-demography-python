from shiny import App, ui, render
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import shinyswatch

poland = gpd.read_file("https://www.gis-support.pl/downloads/2022/powiaty.zip")
poland["powiat_numer"] = poland["JPT_KOD_JE"].astype("int").astype("str")
poland["powiat_nazwa"] = poland["JPT_NAZWA_"].str.replace("powiat ", "")


### CMR yearly data (plus used in deaths data)
ALL_CMR_Y = pd.read_csv(
    "/Users/nelatoma/Documents/icm/magisterka/zgony/MAGISTERKA_OFFICIAL/poviats_code/results/ALL_CMR_Y.csv"
)
ALL_CMR_Y["powiat_numer"] = ALL_CMR_Y["powiat_numer"].astype("str")
poviats_CMR_coord_Y = pd.merge(ALL_CMR_Y, poland, on=["powiat_numer"])
poviats_CMR_coord_Y = poviats_CMR_coord_Y.query('powiat_nazwa != "Wałbrzych"')
poviats_CMR_coord_Y = poviats_CMR_coord_Y.query('powiat_nazwa != "wałbrzyski"')

ALL_CMR_Y_M = pd.read_csv(
    "/Users/nelatoma/Documents/icm/magisterka/zgony/MAGISTERKA_OFFICIAL/poviats_code/results/ALL_CMR_MALES_Y.csv"
)
ALL_CMR_Y_M["powiat_numer"] = ALL_CMR_Y_M["powiat_numer"].astype("str")
poviats_CMR_coord_Y_M = pd.merge(ALL_CMR_Y_M, poland, on=["powiat_numer"])
poviats_CMR_coord_Y_M = poviats_CMR_coord_Y_M.query('powiat_nazwa != "Wałbrzych"')
poviats_CMR_coord_Y_M = poviats_CMR_coord_Y_M.query('powiat_nazwa != "wałbrzyski"')

ALL_CMR_Y_F = pd.read_csv(
    "/Users/nelatoma/Documents/icm/magisterka/zgony/MAGISTERKA_OFFICIAL/poviats_code/results/ALL_CMR_FEMALES_Y.csv"
)
ALL_CMR_Y_F["powiat_numer"] = ALL_CMR_Y_F["powiat_numer"].astype("str")
poviats_CMR_coord_Y_F = pd.merge(ALL_CMR_Y_F, poland, on=["powiat_numer"])
poviats_CMR_coord_Y_F = poviats_CMR_coord_Y_F.query('powiat_nazwa != "Wałbrzych"')
poviats_CMR_coord_Y_F = poviats_CMR_coord_Y_F.query('powiat_nazwa != "wałbrzyski"')

### CMR weekly data (plus used in deaths data)
ALL_CMR_W = pd.read_csv(
    "/Users/nelatoma/Documents/icm/magisterka/zgony/MAGISTERKA_OFFICIAL/poviats_code/results/ALL_CMR_W.csv"
)
ALL_CMR_W["powiat_numer"] = ALL_CMR_W["powiat_numer"].astype("str")
poviats_CMR_coord_W = pd.merge(ALL_CMR_W, poland, on=["powiat_numer"])

ALL_CMR_W_F = pd.read_csv(
    "/Users/nelatoma/Documents/icm/magisterka/zgony/MAGISTERKA_OFFICIAL/poviats_code/results/ALL_CMR_FEMALES_W.csv"
)
ALL_CMR_W_F["powiat_numer"] = ALL_CMR_W_F["powiat_numer"].astype("str")
poviats_CMR_coord_W_F = pd.merge(ALL_CMR_W_F, poland, on=["powiat_numer"])

ALL_CMR_W_M = pd.read_csv(
    "/Users/nelatoma/Documents/icm/magisterka/zgony/MAGISTERKA_OFFICIAL/poviats_code/results/ALL_CMR_MALES_W.csv"
)
ALL_CMR_W_M["powiat_numer"] = ALL_CMR_W_M["powiat_numer"].astype("str")
poviats_CMR_coord_W_M = pd.merge(ALL_CMR_W_M, poland, on=["powiat_numer"])


######
age_groups = [
    "TOTAL",
    "Y_LT5",
    "Y5-9",
    "Y10-14",
    "Y15-19",
    "Y20-24",
    "Y25-29",
    "Y30-34",
    "Y35-39",
    "Y40-44",
    "Y45-49",
    "Y50-54",
    "Y55-59",
    "Y60-64",
    "Y65-69",
    "Y70-74",
    "Y75-79",
    "Y80-84",
    "Y_GE85",
]
genders = ["Total", "Male", "Female"]

#####

app_ui = ui.page_fluid(
    shinyswatch.theme.journal(),
    ui.navset_pill(
        # elements ----
        ui.nav(
            "Yearly",
            # ui.h2("Covid-19 influence on demography of Poland"),
            ui.panel_title("Yearly number of deaths"),
            ui.layout_sidebar(
                ui.panel_sidebar(
                    ui.input_slider(
                        "year", "Year", 2000, 2021, value=2010, step=1, sep=""
                    ),
                    ui.input_select("age_group", "Age group", age_groups),
                    ui.input_radio_buttons("gender", "Gender", genders),
                ),
                ui.panel_main(ui.output_plot("year_plot")),
            ),
        ),
        ui.nav(
            "Weekly",
            ui.panel_title("Weekly number of deaths"),
            ui.layout_sidebar(
                ui.panel_sidebar(
                    ui.input_slider(
                        "year_1", "Year", 2000, 2021, value=2010, step=1, sep=""
                    ),
                    ui.input_slider("week_1", "Week", 1, 52, value=1, step=1),
                    ui.input_select("age_group_1", "Age group", age_groups),
                    ui.input_radio_buttons("gender_1", "Gender", genders),
                ),
                ui.panel_main(ui.output_plot("week_plot")),
            ),
        ),
        ui.nav(
            "Yearly CMR",
            ui.panel_title("Yearly Crude Mortality Rate"),
            ui.markdown(
                """
                Yearly Crude Mortality Rate is a number of deaths in a given year divided by number of people in the population in that year multiplied by 100 000.
            """
            ),
            ui.layout_sidebar(
                ui.panel_sidebar(
                    ui.input_slider(
                        "year_2", "Year", 2000, 2021, value=2010, step=1, sep=""
                    ),
                    # ui.input_slider("week_1", "Week", 1, 52, value=1, step=1),
                    ui.input_select("age_group_2", "Age group", age_groups),
                    ui.input_radio_buttons("gender_2", "Gender", genders),
                ),
                ui.panel_main(ui.output_plot("year_plot_cmr")),
            ),
        ),
        ui.nav(
            "Weekly CMR",
            ui.panel_title("Weekly Crude Mortality Rate"),
            ui.markdown(
                """
                Weekly Crude Mortality Rate is a number of deaths in a given week divided by number of people in the population in that week's year multiplied by 100 000.
                It means that CRM for all weeks of the year have common denominator.
            """
            ),
            ui.layout_sidebar(
                ui.panel_sidebar(
                    ui.input_slider(
                        "year_3", "Year", 2000, 2021, value=2010, step=1, sep=""
                    ),
                    ui.input_slider("week_3", "Week", 1, 52, value=1, step=1),
                    ui.input_select("age_group_3", "Age group", age_groups),
                    ui.input_radio_buttons("gender_3", "Gender", genders),
                ),
                ui.panel_main(
                    ui.output_plot("week_plot_cmr")
                ),
            ),
        ),
    ),
)


def server(input, output, session):
    @output
    @render.plot
    def year_plot():
        current_gender = pd.DataFrame()
        if input.gender() == "Total":
            current_gender = poviats_CMR_coord_Y
        elif input.gender() == "Female":
            current_gender = poviats_CMR_coord_Y_F
        else:
            current_gender = poviats_CMR_coord_Y_M
        year_data = gpd.GeoDataFrame(
            current_gender.query(
                f'year == {input.year()} & age_group == "{input.age_group()}"'
            )
        )
        fig, ax = plt.subplots()
        fig = year_data.plot(ax=ax, column="deaths", cmap="magma_r", legend=True)
        ax.set_title(
            f"Year: {input.year()}, Age group: {input.age_group()}, Gender group: {input.gender()}"
        )
        ax.set_axis_off()
        return fig

    @output
    @render.plot
    def week_plot():
        current_gender = pd.DataFrame()
        week_formatted = f"{input.week_1():02d}"
        if input.gender_1() == "Total":
            current_gender = poviats_CMR_coord_W
        elif input.gender_1() == "Female":
            current_gender = poviats_CMR_coord_W_F
        else:
            current_gender = poviats_CMR_coord_W_M

        week_data = gpd.GeoDataFrame(
            current_gender.query(
                f'year == {input.year_1()} & week == "T{week_formatted}" & age_group == "{input.age_group_1()}"'
            )
        )
        # Create the plot
        fig, ax = plt.subplots(figsize=(20, 20))
        fig = week_data.plot(ax=ax, column="deaths", cmap="magma_r", legend=True)
        ax.set_axis_off()
        ax.set_title(
            f"Year: {input.year_1()}, week: {input.week_1()}, age group: {input.age_group_1()}, gender group: {input.gender_1()}",
        )
        return fig

    @output
    @render.plot
    def year_plot_cmr():
        current_gender = pd.DataFrame()

        if input.gender_2() == "Total":
            current_gender = poviats_CMR_coord_Y
        elif input.gender_2() == "Female":
            current_gender = poviats_CMR_coord_Y_F
        else:
            current_gender = poviats_CMR_coord_Y_M

        year_data = gpd.GeoDataFrame(
            current_gender.query(
                f"year == {input.year_2()} and age_group == '{input.age_group_2()}'"
            )
        )
        fig, ax = plt.subplots()
        fig = year_data.plot(ax=ax, column="CMR", cmap="magma_r", legend=True)
        ax.set_title(
            f"Year: {input.year_2()}, Age group: {input.age_group_2()}, gender: {input.gender_2()}"
        )
        ax.set_axis_off()
        return fig
    
    @output
    @render.plot
    def week_plot_cmr():
        current_gender = pd.DataFrame()
        week_formatted = f"{input.week_3():02d}"

        if input.gender_3() == "Total":
            current_gender = poviats_CMR_coord_W
        elif input.gender_3() == "Female":
            current_gender = poviats_CMR_coord_W_F
        else:
            current_gender = poviats_CMR_coord_W_M

        year_data = gpd.GeoDataFrame(
            current_gender.query(
                f"year == {input.year_3()} and week == 'T{week_formatted}' and age_group == '{input.age_group_3()}'"
            )
        )
        fig, ax = plt.subplots()
        fig = year_data.plot(ax=ax, column="CMR", cmap="magma_r", legend=True)
        ax.set_title(
            f"Year: {input.year_3()}, Age group: {input.age_group_3()}, gender: {input.gender_3()}"
        )
        ax.set_axis_off()
        return fig


app = App(app_ui, server)
