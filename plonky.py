'''
Plonky - the drunken RESTful API tool
'''
from kivy.lang import Builder
from kivymd.app import MDApp

from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem, TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
import os, json, string, random
os.environ['KIVY_GL_BACKEND']='angle_sdl2'

#Project
Builder.load_file('kvs/project/add.kv')
Builder.load_file('kvs/project/card.kv')
Builder.load_file('kvs/project/collection.kv')
Builder.load_file('kvs/project/collection_item.kv')
Builder.load_file('kvs/project/language_selection.kv')

class AddCollection(MDBoxLayout):
    pass
class AddCollectionItem(MDBoxLayout):
    pass
class AddProject(MDBoxLayout):
    pass

class LanguageSelection(OneLineListItem):
    pass

class ProjectCard(MDCard):
    selected = BooleanProperty()
    json = StringProperty()
    file = StringProperty()
    text = StringProperty()
    name = StringProperty()
    icon = StringProperty()

class ProjectCollection(MDBoxLayout):
    pass

class ProjectCollectionItem(MDBoxLayout):
    pass

# Request box
Builder.load_file('kvs/request/tabs/params.kv')
Builder.load_file('kvs/request/tabs/auth.kv')
Builder.load_file('kvs/request/tabs/headers.kv')
Builder.load_file('kvs/request/tabs/body.kv')
Builder.load_file('kvs/request/tabs/globals.kv')

class RequestTabParams(MDFloatLayout, MDTabsBase):
    pass
class RequestTabParamsListItem(MDBoxLayout):
    pass

class RequestTabAuth(MDFloatLayout, MDTabsBase):
    pass
class RequestTabBody(MDFloatLayout, MDTabsBase):
    pass
class RequestTabHeaders(MDFloatLayout, MDTabsBase):
    pass
class RequestTabGlobals(MDFloatLayout, MDTabsBase):
    pass

# Response box
Builder.load_file('kvs/response/tabs/body.kv')
Builder.load_file('kvs/response/tabs/headers.kv')

class ResponseTabBody(MDFloatLayout, MDTabsBase):
    pass
class ResponseTabHeaders(MDFloatLayout, MDTabsBase):
    pass

Builder.load_file('kvs/app.kv')

class ContentNavigationDrawer(MDBoxLayout):
    pass

class App(Widget):
    pass

class MainApp(MDApp):
    add_project_dialog = None
    add_project_collection_dialog = None
    add_project_collection_item_dialog = None

    alert = None
    cfg_folder = "cfg/"
    projects_folder = "projects/"
    selected_icon = "application-outline"

    selected_collection = None
    selected_project = None
    selected_request = None

    projects = []
    speed_dial = None
    speed_menu = {}
    rail_height = 200
    project_changed = False

    request_tab_globals = None
    request_tab_params = None
    request_tab_auth = None
    request_tab_headers = None
    request_tab_body = None

    def build(self):
        self.title = "Plonky"
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"

        self.speed_menu = {
            'Add project': [
                'shape-square-rounded-plus',
                "on_press", lambda x: self.add_project()
            ]
        }

        return App()

    def on_start(self):
        # Build request tabs
        self.request_tab_params = RequestTabParams()
        self.root.ids.request_tabs.add_widget(self.request_tab_params)

        self.request_tab_auth = RequestTabAuth()
        self.root.ids.request_tabs.add_widget(self.request_tab_auth)

        self.request_tab_headers = RequestTabHeaders()
        self.root.ids.request_tabs.add_widget(self.request_tab_headers)

        self.request_tab_body = RequestTabBody()
        self.root.ids.request_tabs.add_widget(self.request_tab_body)

        self.request_tab_globals = RequestTabGlobals()
        self.root.ids.request_tabs.add_widget(self.request_tab_globals)

        # Build response tabs
        self.root.ids.response_tabs.add_widget(ResponseTabBody())
        self.root.ids.response_tabs.add_widget(ResponseTabHeaders())

        # Build the request type menu
        self.request_type_menu = MDDropdownMenu(
            caller = self.root.ids.request_type,
            items = [
            {
                "viewclass": "OneLineListItem",
                "text": "GET",
                "height": dp(56),
                "on_release": lambda x="GET": self.change_type(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "POST",
                "height": dp(56),
                "on_release": lambda x="POST": self.change_type(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "PUT",
                "height": dp(56),
                "on_release": lambda x="PUT": self.change_type(x),
            }
            ,
            {
                "viewclass": "OneLineListItem",
                "text": "PATCH",
                "height": dp(56),
                "on_release": lambda x="PATCH": self.change_type(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "DELETE",
                "height": dp(56),
                "on_release": lambda x="DELETE": self.change_type(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "COPY",
                "height": dp(56),
                "on_release": lambda x="COPY": self.change_type(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "HEAD",
                "height": dp(56),
                "on_release": lambda x="HEAD": self.change_type(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "OPTIONS",
                "height": dp(56),
                "on_release": lambda x="OPTIONS": self.change_type(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "LINK",
                "height": dp(56),
                "on_release": lambda x="LINK": self.change_type(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "UNLINK",
                "height": dp(56),
                "on_release": lambda x="UNLINK": self.change_type(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "PURGE",
                "height": dp(56),
                "on_release": lambda x="PURGE": self.change_type(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "LOCK",
                "height": dp(56),
                "on_release": lambda x="LOCK": self.change_type(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "UNLOCK",
                "height": dp(56),
                "on_release": lambda x="UNLOCK": self.change_type(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "PROPFIND",
                "height": dp(56),
                "on_release": lambda x="PROPFIND": self.change_type(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "VIEW",
                "height": dp(56),
                "on_release": lambda x="VIEW": self.change_type(x),
            }
        ],
            position = "center",
            width_mult = 4,
        )
        self.request_type_menu.bind()        

        self.load_projects()

    def change_type(self, type):
        self.root.ids.request_type.set_item(type)
        self.request_type_menu.dismiss()

    def create_alert(self, title, text):
        self.alert = MDDialog(
            title = title,
            text = text,
            buttons =[
                MDFlatButton(
                    text = "CANCEL",
                    theme_text_color = "Custom",
                    text_color = self.theme_cls.primary_color,
                    on_release = self.close_alert
                ),
                MDFlatButton(
                    text = "OK",
                    theme_text_color = "Custom",
                    text_color = self.theme_cls.primary_color,
                    on_release = self.close_alert
                ),
            ],
        )

        self.alert.open()

    def create_toast(self, text, type = "normal"):
        if (type == "error"):
            bg_colour = "#B00020"
            text_color = "white"
        elif (type == "warning"):
            bg_colour = "#FFDE03"
            text_color = "black"
        else:
            bg_colour = self.theme_cls.primary_color
            text_color = "white"

        MDSnackbar(
            MDLabel(
                text = text,                
                theme_text_color = "Custom",
                text_color = text_color
            ),
            y = dp(24),
            pos_hint = {"center_x": 0.5},
            size_hint_x = 0.5,
            md_bg_color = bg_colour
        ).open()

    def close_alert(self, *args):
        if self.alert:
            self.alert.dismiss()
            self.alert = None

    # Generate a random string, used for IDs and filenames
    def random_string(self):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(24))

    # Select from the navigation
    def rail_select(self, instance_navigation_rail, instance_navigation_rail_item):
        if instance_navigation_rail_item.text.lower() == "projects":
            self.root.ids.projects_drawer.set_state("open")

    def trigger_send(self):
        print("send")

#--- Project ---
    def add_project_to_rail(self, project):
        card = ProjectCard(
            selected = False,
            json = json.dumps(project),
            text = project["name"],
            file = project["file"],
            icon = project["icon"]
        )
        self.root.ids.rail.add_widget(card)
        self.selected_project = card
        
    def add_project(self):
        if self.project_changed:
            self.project_save_prompt("add_project")
            return
        
        if not self.add_project_dialog:
            layout = AddProject()

            #Load the JSON for the selection
            with open(self.cfg_folder + "language_selection.json") as file_json:
                menu_items = json.load(file_json)
            for item in menu_items:
                item["height"] =  dp(56)
                item["viewclass"] = "LanguageSelection"
                item["on_release"] = lambda x=item["text"], icon=item["icon"]: self.add_project_lang_selected(x, icon)

            #Generate the language selection box
            self.lang_selection_menu = MDDropdownMenu(
                caller = layout.ids.drop_item,
                items = menu_items,
                position = "center",
                width_mult = 4,
            )
            self.lang_selection_menu.bind()

            #Build the Add new project dialog box
            self.add_project_dialog = MDDialog(
                title = "Add new project",
                content_cls = layout,
                type = "custom",
                buttons = [
                    MDFlatButton(
                        text = "CANCEL",
                        theme_text_color = "Custom",
                        text_color = self.theme_cls.primary_color,
                        on_release = self.cancel_add_project
                    ),
                    MDFlatButton(
                        text = "OK",
                        theme_text_color = "Custom",
                        text_color = self.theme_cls.primary_color,
                        on_release = self.create_project
                    )
                ]
            )
        self.add_project_dialog.open()

    def add_project_collection(self):
        if not self.add_project_collection_dialog:
            layout = AddCollection()

            #Build the Add new project collection dialog box
            self.add_project_collection_dialog = MDDialog(
                title = "Add new collection",
                content_cls = layout,
                type = "custom",
                buttons = [
                    MDFlatButton(
                        text = "CANCEL",
                        theme_text_color = "Custom",
                        text_color = self.theme_cls.primary_color,
                        on_release = self.cancel_add_project_collection
                    ),
                    MDFlatButton(
                        text = "OK",
                        theme_text_color = "Custom",
                        text_color = self.theme_cls.primary_color,
                        on_release = self.create_project_collection
                    )
                ]
            )
        self.add_project_collection_dialog.open()

    def add_project_collection_item(self):
        if not self.selected_collection:
            self.create_toast(f"Please select a collection first", "error")
            return

        if not self.add_project_collection_item_dialog:
            layout = AddCollectionItem()

            #Build the Add new project collection item dialog box
            self.add_project_collection_item_dialog = MDDialog(
                title = "Add new collection",
                content_cls = layout,
                type = "custom",
                buttons = [
                    MDFlatButton(
                        text = "CANCEL",
                        theme_text_color = "Custom",
                        text_color = self.theme_cls.primary_color,
                        on_release = self.cancel_add_project_collection_item
                    ),
                    MDFlatButton(
                        text = "OK",
                        theme_text_color = "Custom",
                        text_color = self.theme_cls.primary_color,
                        on_release = self.create_project_collection_item
                    )
                ]
            )
        self.add_project_collection_item_dialog.open()

    def add_project_lang_selected(self, text_item, icon):
        self.add_project_dialog.content_cls.ids.drop_item.set_item(text_item)
        self.selected_icon = icon
        self.lang_selection_menu.dismiss()

    # Build the project UI, the collections, etc
    def build_project_ui(self, project):
        self.root.ids.project.clear_widgets()
        
        if project["collections"]:
            if self.speed_dial:
                self.root.ids.app_screen.remove_widget(self.speed_dial)

            self.speed_dial = MDFloatingActionButtonSpeedDial()
            self.speed_dial.data = {
                'Add collection': [
                    'folder-plus-outline',
                    "on_press", lambda x: self.add_project_collection()
                ],
                'Add request': [
                    'cloud-plus-outline',
                    "on_press", lambda x: self.add_project_collection_item()
                ],
                'Add project': [
                    'shape-square-rounded-plus',
                    "on_press", lambda x: self.add_project()
                ]
            }
            self.speed_dial.root_button_anim = True
            self.root.ids.app_screen.add_widget(self.speed_dial)
            
        self.build_collection(project)

        self.clear_tabs()

        for param in project["globals"]:
            request_param = RequestTabParamsListItem()
            request_param.ids.param_key.text = param["key"]
            request_param.ids.param_value.text = param["value"]
            request_param.ids.param_active.active = param["active"]
            request_param.ids.param_active.bind(active=self.on_request_param_change)
            self.request_tab_globals.ids.globals.add_widget(request_param)
        
        self.request_tab_globals.ids.param_add_btn.opacity = 1
    
    def build_collection(self, project):
        self.root.ids.project.clear_widgets()
        
        for collection_data in project["collections"]:
            collection = ProjectCollection()
                        
            for item_data in collection_data["items"]:
                if item_data["type"].upper() == "POST":
                    icon_type = "upload-outline"
                else:
                    icon_type = "download-outline"
                
                item = ProjectCollectionItem()
                item.add_widget(
                    TwoLineAvatarIconListItem(
                        IconLeftWidget(
                            icon = icon_type
                        ),
                        IconRightWidget(
                            id = item_data["id"],
                            icon = "close",
                            on_release = lambda x: self.delete_project_collection_item_promt(x)
                        ),
                        id = item_data["id"],
                        text = item_data["name"],
                        secondary_text = item_data["type"].upper(),
                        on_release = lambda x,
                            title = f"{collection_data['name']} > {item_data['name']}",
                            type = item_data["type"].upper(),
                            url = item_data["url"]:
                                self.select_project_collection_item(x, title, type, url)
                    )
                )

                collection.ids.collection_items.add_widget(item)

            self.root.ids.project.add_widget(MDExpansionPanel(
                icon = "folder-outline",
                content = collection,
                panel_cls = MDExpansionPanelOneLine (
                    text = collection_data['name'],
                    id = collection_data['id'],
                    on_release = lambda x: self.select_project_collection(x)
                )
            ))

    def cancel_add_project(self, *args):
        self.reset_add_project()
        self.add_project_dialog.dismiss()
    def cancel_add_project_collection(self, *args):
        self.reset_add_project_collection()
        self.add_project_collection_dialog.dismiss()
    def cancel_add_project_collection_item(self, *args):
        self.reset_add_project_collection_item()
        self.add_project_collection_item_dialog.dismiss()

    def clear_tabs(self):
        self.root.ids.request_type.opacity = 0
        self.root.ids.request_url.opacity = 0

        self.root.ids.current_project_item.title = "Please select a request"

        self.request_tab_params.ids.request_params.clear_widgets()
        self.request_tab_auth.ids.request_params.clear_widgets()
        self.request_tab_headers.ids.request_params.clear_widgets()
        self.request_tab_body.ids.request_params.clear_widgets()

        self.root.ids.current_project_item.right_action_items = [
            ["content-save-outline", lambda x: self.save_project()]
        ]

    def close_save_alert(self, from_func, arg):
        self.alert.dismiss()
        self.alert = None
        self.project_changed = False
        func = getattr(self, from_func)
        func(arg)

    def create_project(self, *args):
        # Random filename
        filename = self.random_string() + ".json"
        
        file = f"{self.projects_folder}" + filename
        selected_lang = self.selected_icon.replace("language-", "")
        
        project = {}
        project["name"] = self.add_project_dialog.content_cls.ids.text_project.text
        project["lang"] = selected_lang
        project["icon"] = self.selected_icon
        project["project"] = {}
        
        # create the project file
        with open(file, 'w') as fp:
            fp.write(json.dumps(project))

        project["file"] = file
        self.projects.append(project)

        self.add_project_to_rail(project)
        
        self.cancel_add_project()
        self.speed_dial.close_stack()

        self.create_toast("Project created")
        self.project_changed = True

    def create_project_collection(self, *args):
        project = json.loads(self.selected_project.json)
        project["collections"].append({"id": self.random_string(), "name": self.add_project_collection_dialog.content_cls.ids.text_collection_name.text, "items": []})
        self.project_changed = True

        self.build_collection(project)
        self.selected_project.json = json.dumps(project)

        self.cancel_add_project_collection(args)
        self.speed_dial.close_stack()

        self.create_toast(f"Project collection created")
    
    def create_project_collection_item(self, *args):
        project = json.loads(self.selected_project.json)
        self.project_changed = True

        self.build_collection(project)
        self.selected_project.json = json.dumps(project)

        self.cancel_add_project_collection_item(args)
        self.speed_dial.close_stack()

        self.create_toast(f"Request created")

    # Delete the project
    def delete_project(self, *args):
        try:
            if self.selected_project:
                self.root.ids.rail.remove_widget(self.selected_project)
                os.remove(self.selected_project.file)
                self.selected_project = None
                
                self.root.ids.current_project.title = "Please select a project"
                self.root.ids.current_project.right_action_items = []
                self.root.ids.project.clear_widgets()
                self.root.ids.project_drawer.set_state("close")

                self.request_tab_params.ids.request_params.clear_widgets()
                self.request_tab_auth.ids.request_params.clear_widgets()
                self.request_tab_headers.ids.request_params.clear_widgets()
                self.request_tab_body.ids.request_params.clear_widgets()

                self.close_alert()

                self.create_toast("Project deleted")
        except:
            self.close_alert()
            self.create_alert("Delete error", "Failed to delete the project")

    # Delete the collection item from the project
    def delete_project_collection_item(self, item):
        self.project_changed = True

        project = json.loads(self.selected_project.json)
        for collection in project["collections"]:
            collection_key = 0
            for collection_item in collection["items"]:
                if (collection_item["id"] == item.id):
                    project["collections"][collection_key]["items"].remove(collection_item)
                collection_key += 1

        self.build_collection(project)
        self.clear_tabs()

        self.create_toast(f"Project collection request has been deleted", "warning")
        self.close_alert()

    # Prompt before deleting the collection item
    def delete_project_collection_item_promt(self, item):
        self.alert = MDDialog(
            title = "Delete collection request",
            text = "Are you sure?",
            buttons = [
                MDFlatButton(
                    text = "NO",
                    theme_text_color = "Custom",
                    text_color = self.theme_cls.primary_color,
                    on_release = self.close_alert
                ),
                MDFlatButton(
                    text = "YES",
                    theme_text_color = "Custom",
                    text_color = self.theme_cls.primary_color,
                    on_release = lambda x, id = id: self.delete_project_collection_item(item)
                )
            ]
        )
        self.alert.open()

    # Prompt before deleting the project
    def delete_project_prompt(self, *args):
        if self.selected_project:
            self.alert = MDDialog(
                title = "Delete project",
                text = "Are you sure?",
                buttons = [
                    MDFlatButton(
                        text = "NO",
                        theme_text_color = "Custom",
                        text_color = self.theme_cls.primary_color,
                        on_release = self.close_alert
                    ),
                    MDFlatButton(
                        text = "YES",
                        theme_text_color = "Custom",
                        text_color = self.theme_cls.primary_color,
                        on_release = self.delete_project
                    )
                ]
            )

            self.alert.open()
        else:
            self.create_alert("Delete error", "No project has been selected")

    # Load the projects from the projects folder
    def load_projects(self):
        self.projects = []
        
        #Read the projects json files
        for i, file in enumerate(os.listdir("projects")):
            if file.endswith(".json"):
                with open(self.projects_folder + file) as file_json:
                    try:
                        project = json.load(file_json)
                        project["file"] = self.projects_folder + file

                        self.add_project_to_rail(project)
                        self.projects.append(project)

                    except Exception as err:
                        self.create_toast(f"Failed to load the project json for {file}", "error")
                        print(f"Unexpected {err=}, {type(err)=}")

        if self.selected_project:
            self.select_project(self.selected_project)

    # Prompt before deleting the project
    def project_save_prompt(self, from_func, arg):
        self.alert = MDDialog(
            title = "Save project",
            text = "The projec has changed, would you like to save it?",
            buttons = [
                MDFlatButton(
                    text = "NO",
                    theme_text_color = "Custom",
                    text_color = self.theme_cls.primary_color,
                    on_release = lambda x: self.close_save_alert(from_func, arg)
                ),
                MDFlatButton(
                    text = "YES",
                    theme_text_color = "Custom",
                    text_color = self.theme_cls.primary_color,
                    on_release = lambda x: self.save_project(from_func, arg)
                )
            ]
        )

        self.alert.open()

    def reset_add_project(self):
        self.add_project_dialog.content_cls.ids.text_project.text = ""
    def reset_add_project_collection(self):
        self.add_project_collection_dialog.content_cls.ids.text_collection_name.text = ""
    def reset_add_project_collection_item(self):
        self.add_project_collection_item_dialog.content_cls.ids.text_collection_item_name.text = ""

    # Save the project
    def save_project(self, from_func = None, arg = None):
        if not self.selected_project:
            self.create_toast("No project to save", "error")
            return
        
        self.close_alert()

        project = json.loads(self.selected_project.json)
        
        if self.selected_collection:
            try:
                collection_id = self.selected_collection.id
                if self.request_tab_params.ids.request_params.children:
                    for collection in project["collections"]:
                        if collection_id == collection["id"]:
                            for collection_item in collection["items"]:
                                if collection_item["id"] == self.selected_request.id:
                                    collection_item["params"] = []
                                    for param in self.request_tab_params.ids.request_params.children:
                                        if param.ids.param_key.text and param.ids.param_value.text:
                                            collection_item["params"].append({
                                                "key": param.ids.param_key.text,
                                                "value": param.ids.param_value.text,
                                                "active": param.ids.param_active.active
                                            })

                                    collection_item["auth"] = []
                                    for param in self.request_tab_auth.ids.request_params.children:
                                        if param.ids.param_key.text and param.ids.param_value.text:
                                            collection_item["auth"].append({
                                                "key": param.ids.param_key.text,
                                                "value": param.ids.param_value.text,
                                                "active": param.ids.param_active.active
                                            })

                                    collection_item["headers"] = []
                                    for param in self.request_tab_headers.ids.request_params.children:
                                        if param.ids.param_key.text and param.ids.param_value.text:
                                            collection_item["headers"].append({
                                                "key": param.ids.param_key.text,
                                                "value": param.ids.param_value.text,
                                                "active": param.ids.param_active.active
                                            })

                                    collection_item["body"] = []
                                    for param in self.request_tab_body.ids.request_params.children:
                                        if param.ids.param_key.text and param.ids.param_value.text:
                                            collection_item["body"].append({
                                                "key": param.ids.param_key.text,
                                                "value": param.ids.param_value.text,
                                                "active": param.ids.param_active.active
                                            })
                            break
            except:
                self.create_toast("Failed save the request parameters", "error")

        if self.request_tab_globals.ids.globals.children:
            project["globals"] = []
            for param in self.request_tab_globals.ids.globals.children:
                if param.ids.param_key.text and param.ids.param_value.text:
                    project["globals"].append({
                        "key": param.ids.param_key.text,
                        "value": param.ids.param_value.text,
                        "active": param.ids.param_active.active
                    })

        file = project["file"]
        del project["file"]

        print(project["collections"])

        # create the project file
        with open(file, 'w') as fp:
            fp.write(json.dumps(project))

        self.create_toast("Project saved")
        self.project_changed = False

        if from_func:
            func = getattr(self, from_func)
            func(arg)

    # Select a project from the popout
    def select_project(self, card):
        if self.project_changed:
            self.project_save_prompt("select_project", card)
            return
        
        project = json.loads(card.json)
        
        if card.selected:
            self.create_toast(f"Project {project['name']} already selected", "warning")
            self.root.ids.projects_drawer.set_state("close")
            return
        
        for child in self.root.ids.rail.children:
            child.md_bg_color = self.theme_cls.primary_color
            child.ids.icon.md_bg_color: self.theme_cls.primary_color
            child.ids.label.color = self.theme_cls.primary_light
            child.selected = False

        card.md_bg_color = self.theme_cls.primary_light
        card.ids.icon.md_bg_color: self.theme_cls.primary_light
        card.ids.label.color = self.theme_cls.primary_dark
        card.selected = True

        self.root.ids.current_project.title = project["name"]
        self.root.ids.current_project.right_action_items = [
            [project["icon"]],
            ["dots-vertical", lambda x: self.root.ids.project_drawer.set_state("open")]
        ]

        self.selected_project = card
        self.build_project_ui(project)

        self.root.ids.projects_drawer.set_state("close")

        self.root.ids.current_project_item.right_action_items = [
            ["content-save-outline", lambda x: self.save_project()]
        ]
        
        self.create_toast(f"Project {project['name']} selected")

    def select_project_collection(self, collection):
        self.selected_collection = collection

    def select_project_collection_item(self, item, title, type, url):
        self.clear_tabs()

        self.root.ids.current_project_item.title = title
        self.root.ids.request_type.set_item(type)
        self.root.ids.request_url.hint_text = ""
        self.root.ids.request_url.text = url
        self.selected_request = item

        project = json.loads(self.selected_project.json)

        self.root.ids.current_project_item.right_action_items = [
            ["content-save-outline", lambda x: self.save_project()],
            ["send-circle", lambda x: self.trigger_send()]
        ]

        self.root.ids.request_type.opacity = 1
        self.root.ids.request_url.opacity = 1

        collection_id = self.selected_collection.id
        try:
            for collection in project["collections"]:
                if collection_id == collection["id"]:
                    for collection_item in collection["items"]:
                        if collection_item["id"] == item.id:
                            for param in collection_item["params"]:
                                request_param = RequestTabParamsListItem()
                                request_param.ids.param_key.text = param["key"]
                                request_param.ids.param_value.text = param["value"]
                                request_param.ids.param_active.active = param["active"]
                                request_param.ids.param_active.bind(active=self.on_request_param_change)
                                self.request_tab_params.ids.request_params.add_widget(request_param)

                            for param in collection_item["auth"]:
                                request_param = RequestTabParamsListItem()
                                request_param.ids.param_key.text = param["key"]
                                request_param.ids.param_value.text = param["value"]
                                request_param.ids.param_active.active = param["active"]
                                request_param.ids.param_active.bind(active=self.on_request_param_change)
                                self.request_tab_auth.ids.request_params.add_widget(request_param)

                            for param in collection_item["headers"]:
                                request_param = RequestTabParamsListItem()
                                request_param.ids.param_key.text = param["key"]
                                request_param.ids.param_value.text = param["value"]
                                request_param.ids.param_active.active = param["active"]
                                request_param.ids.param_active.bind(active=self.on_request_param_change)
                                self.request_tab_headers.ids.request_params.add_widget(request_param)

                            for param in collection_item["body"]:
                                request_param = RequestTabParamsListItem()
                                request_param.ids.param_key.text = param["key"]
                                request_param.ids.param_value.text = param["value"]
                                request_param.ids.param_active.active = param["active"]
                                request_param.ids.param_active.bind(active=self.on_request_param_change)
                                self.request_tab_body.ids.request_params.add_widget(request_param)
        except:
            if collection_item != None:
                collection_item["params"] = []
                collection_item["auth"] = []
                collection_item["headers"] = []
                collection_item["body"] = []
            self.create_toast("Failed to fully process the project", "error")

        self.request_tab_params.ids.param_add_btn.opacity = 1
        self.request_tab_auth.ids.param_add_btn.opacity = 1
        self.request_tab_headers.ids.param_add_btn.opacity = 1
        self.request_tab_body.ids.param_add_btn.opacity = 1

#--- END Project ---
    
#--- Request params ---

    # Add a request parameter to the project
    def add_request_param(self, btn):
        if not self.selected_project:
            self.create_toast("No request option selected", "error")
            return
        self.request_tab_params.ids.request_params.add_widget(RequestTabParamsListItem(id=self.selected_request.id))

    # Delete the request parameter
    def delete_request_param(self, item):
        self.request_tab_params.ids.request_params.remove_widget(item)    

    # When a request parameter is changed
    def on_request_param_change(self, checkbox = None, value = None):
        self.project_changed = True
        print("here")
    
#--- END Request params ---

#--- Request auth ---

    # Add a request auth to the project
    def add_request_auth(self, btn):
        if not self.selected_project:
            self.create_toast("No project selected", "error")
            return
        
        self.request_tab_auth.ids.request_params.add_widget(RequestTabParamsListItem(id=self.selected_project.id))

#--- END Request auth ---

#--- Request headers ---

    # Add a request headers to the project
    def add_request_header(self, btn):
        if not self.selected_project:
            self.create_toast("No project selected", "error")
            return
        
        self.request_tab_headers.ids.request_params.add_widget(RequestTabParamsListItem(id=self.selected_project.id))

#--- END Request headers ---

#--- Request body ---

    # Add a request headers to the project
    def add_request_body(self, btn):
        if not self.selected_project:
            self.create_toast("No project selected", "error")
            return
        
        self.request_tab_body.ids.request_params.add_widget(RequestTabParamsListItem(id=self.selected_project.id))

#--- END Request body ---

#--- Globals ---

    # Add a request global to the project
    def add_global(self, btn):
        if not self.selected_project:
            self.create_toast("No project selected", "error")
            return
        
        self.request_tab_globals.ids.globals.add_widget(RequestTabParamsListItem(id=self.selected_project.id))

#--- END Globals ---


if __name__ == '__main__':
    MainApp().run()