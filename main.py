#!/usr/bin/env python3
"""
Boutique Cosmétique - Application de gestion
Développée avec Python + Kivy / KivyMD
"""

from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTrailingCheckbox
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard

import database as db

# Set a reasonable window size for desktop
Window.size = (1100, 700)

KV = '''
#:import dp kivy.metrics.dp

<LoginScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor
        padding: dp(40)
        spacing: dp(20)

        Widget:
            size_hint_y: 0.15

        MDLabel:
            text: "💄 Boutique Cosmétique"
            font_style: "Headline"
            role: "medium"
            halign: "center"
            adaptive_height: True

        MDLabel:
            text: "Gestion de magasin"
            font_style: "Title"
            role: "medium"
            halign: "center"
            theme_text_color: "Secondary"
            adaptive_height: True

        Widget:
            size_hint_y: 0.05

        MDCard:
            orientation: "vertical"
            padding: dp(30)
            spacing: dp(15)
            size_hint: None, None
            size: dp(380), dp(280)
            pos_hint: {"center_x": 0.5}
            elevation: 2
            radius: [dp(16)]

            MDTextField:
                id: username
                hint_text: "Nom d'utilisateur"
                mode: "outlined"
                text: "admin"

            MDTextField:
                id: password
                hint_text: "Mot de passe"
                mode: "outlined"
                password: True
                text: "admin123"

            MDButton:
                style: "filled"
                pos_hint: {"center_x": 0.5}
                on_release: root.do_login()
                MDButtonText:
                    text: "Se connecter"

        MDLabel:
            text: "Identifiants par défaut : admin / admin123"
            font_style: "Label"
            role: "small"
            halign: "center"
            theme_text_color: "Secondary"
            adaptive_height: True

        Widget:
            size_hint_y: 0.2


<DashboardScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor

        # Top bar
        MDBoxLayout:
            adaptive_height: True
            padding: [dp(16), dp(12)]
            spacing: dp(12)
            md_bg_color: app.theme_cls.primaryContainerColor

            MDIconButton:
                icon: "menu"
                on_release: root.toggle_menu()

            MDLabel:
                text: "Tableau de bord"
                font_style: "Title"
                role: "large"
                adaptive_height: True
                pos_hint: {"center_y": 0.5}

            Widget:

            MDLabel:
                id: user_label
                text: ""
                font_style: "Label"
                role: "large"
                adaptive_size: True
                pos_hint: {"center_y": 0.5}

            MDIconButton:
                icon: "logout"
                on_release: app.logout()

        # Content
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(20)
                spacing: dp(16)
                adaptive_height: True

                # Stats cards row
                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(12)
                    size_hint_y: None
                    height: dp(110)

                    MDCard:
                        orientation: "vertical"
                        padding: dp(16)
                        spacing: dp(4)
                        radius: [dp(12)]
                        MDLabel:
                            text: "Produits"
                            font_style: "Label"
                            role: "medium"
                            theme_text_color: "Secondary"
                            adaptive_height: True
                        MDLabel:
                            id: stat_products
                            text: "0"
                            font_style: "Headline"
                            role: "small"
                            adaptive_height: True

                    MDCard:
                        orientation: "vertical"
                        padding: dp(16)
                        spacing: dp(4)
                        radius: [dp(12)]
                        MDLabel:
                            text: "Stock bas"
                            font_style: "Label"
                            role: "medium"
                            theme_text_color: "Secondary"
                            adaptive_height: True
                        MDLabel:
                            id: stat_low_stock
                            text: "0"
                            font_style: "Headline"
                            role: "small"
                            theme_text_color: "Error"
                            adaptive_height: True

                    MDCard:
                        orientation: "vertical"
                        padding: dp(16)
                        spacing: dp(4)
                        radius: [dp(12)]
                        MDLabel:
                            text: "Clients"
                            font_style: "Label"
                            role: "medium"
                            theme_text_color: "Secondary"
                            adaptive_height: True
                        MDLabel:
                            id: stat_customers
                            text: "0"
                            font_style: "Headline"
                            role: "small"
                            adaptive_height: True

                    MDCard:
                        orientation: "vertical"
                        padding: dp(16)
                        spacing: dp(4)
                        radius: [dp(12)]
                        MDLabel:
                            text: "Ventes du jour"
                            font_style: "Label"
                            role: "medium"
                            theme_text_color: "Secondary"
                            adaptive_height: True
                        MDLabel:
                            id: stat_sales_today
                            text: "0 €"
                            font_style: "Headline"
                            role: "small"
                            adaptive_height: True

                # Quick actions
                MDLabel:
                    text: "Actions rapides"
                    font_style: "Title"
                    role: "medium"
                    adaptive_height: True
                    padding: [0, dp(8), 0, 0]

                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(12)

                    MDButton:
                        style: "filled"
                        on_release: app.go_to("products")
                        MDButtonText:
                            text: "📦 Produits"

                    MDButton:
                        style: "filled"
                        on_release: app.go_to("sales")
                        MDButtonText:
                            text: "🛒 Nouvelle vente"

                    MDButton:
                        style: "filled"
                        on_release: app.go_to("customers")
                        MDButtonText:
                            text: "👥 Clients"

                    MDButton:
                        style: "outlined"
                        on_release: app.go_to("history")
                        MDButtonText:
                            text: "📊 Historique"

                # Low stock alert
                MDLabel:
                    text: "Alertes stock bas"
                    font_style: "Title"
                    role: "medium"
                    adaptive_height: True
                    padding: [0, dp(12), 0, 0]

                MDBoxLayout:
                    id: low_stock_list
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: dp(6)


<ProductsScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor

        MDBoxLayout:
            adaptive_height: True
            padding: [dp(16), dp(12)]
            spacing: dp(12)
            md_bg_color: app.theme_cls.primaryContainerColor

            MDIconButton:
                icon: "arrow-left"
                on_release: app.go_to("dashboard")

            MDLabel:
                text: "Produits"
                font_style: "Title"
                role: "large"
                adaptive_height: True
                pos_hint: {"center_y": 0.5}

            Widget:

            MDIconButton:
                icon: "plus"
                on_release: root.open_add_dialog()

        MDBoxLayout:
            adaptive_height: True
            padding: [dp(16), dp(8)]
            spacing: dp(10)

            MDTextField:
                id: search_field
                hint_text: "Rechercher (nom, marque, code-barres)..."
                mode: "outlined"
                size_hint_x: 0.7
                on_text: root.filter_products(self.text)

            MDButton:
                style: "tonal"
                on_release: root.refresh()
                MDButtonText:
                    text: "Actualiser"

        ScrollView:
            MDBoxLayout:
                id: products_list
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(8)
                adaptive_height: True


<SalesScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor

        MDBoxLayout:
            adaptive_height: True
            padding: [dp(16), dp(12)]
            spacing: dp(12)
            md_bg_color: app.theme_cls.primaryContainerColor

            MDIconButton:
                icon: "arrow-left"
                on_release: app.go_to("dashboard")

            MDLabel:
                text: "Nouvelle vente"
                font_style: "Title"
                role: "large"
                adaptive_height: True
                pos_hint: {"center_y": 0.5}

        MDBoxLayout:
            orientation: "horizontal"
            padding: dp(12)
            spacing: dp(12)

            # Left: product search & list
            MDBoxLayout:
                orientation: "vertical"
                size_hint_x: 0.55
                spacing: dp(8)

                MDTextField:
                    id: product_search
                    hint_text: "Rechercher un produit..."
                    mode: "outlined"
                    on_text: root.search_products(self.text)

                ScrollView:
                    MDBoxLayout:
                        id: available_products
                        orientation: "vertical"
                        adaptive_height: True
                        spacing: dp(4)

            # Right: cart
            MDCard:
                orientation: "vertical"
                size_hint_x: 0.45
                padding: dp(12)
                spacing: dp(8)
                radius: [dp(12)]

                MDLabel:
                    text: "Panier"
                    font_style: "Title"
                    role: "medium"
                    adaptive_height: True

                ScrollView:
                    MDBoxLayout:
                        id: cart_items
                        orientation: "vertical"
                        adaptive_height: True
                        spacing: dp(4)

                MDLabel:
                    id: cart_total
                    text: "Total : 0.00 €"
                    font_style: "Title"
                    role: "large"
                    adaptive_height: True
                    halign: "right"

                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(8)

                    MDButton:
                        style: "outlined"
                        on_release: root.clear_cart()
                        MDButtonText:
                            text: "Vider"

                    MDButton:
                        style: "filled"
                        on_release: root.checkout()
                        MDButtonText:
                            text: "Valider la vente"


<CustomersScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor

        MDBoxLayout:
            adaptive_height: True
            padding: [dp(16), dp(12)]
            spacing: dp(12)
            md_bg_color: app.theme_cls.primaryContainerColor

            MDIconButton:
                icon: "arrow-left"
                on_release: app.go_to("dashboard")

            MDLabel:
                text: "Clients"
                font_style: "Title"
                role: "large"
                adaptive_height: True
                pos_hint: {"center_y": 0.5}

            Widget:

            MDIconButton:
                icon: "plus"
                on_release: root.open_add_dialog()

        MDBoxLayout:
            adaptive_height: True
            padding: [dp(16), dp(8)]

            MDTextField:
                id: search_field
                hint_text: "Rechercher un client..."
                mode: "outlined"
                on_text: root.filter_customers(self.text)

        ScrollView:
            MDBoxLayout:
                id: customers_list
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(8)
                adaptive_height: True


<HistoryScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor

        MDBoxLayout:
            adaptive_height: True
            padding: [dp(16), dp(12)]
            spacing: dp(12)
            md_bg_color: app.theme_cls.primaryContainerColor

            MDIconButton:
                icon: "arrow-left"
                on_release: app.go_to("dashboard")

            MDLabel:
                text: "Historique des ventes"
                font_style: "Title"
                role: "large"
                adaptive_height: True
                pos_hint: {"center_y": 0.5}

            Widget:

            MDIconButton:
                icon: "refresh"
                on_release: root.refresh()

        ScrollView:
            MDBoxLayout:
                id: sales_list
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(8)
                adaptive_height: True
'''


class LoginScreen(Screen):
    def do_login(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        user = db.authenticate(username, password)
        if user:
            app = MDApp.get_running_app()
            app.current_user = user
            app.root.transition = SlideTransition(direction="left")
            app.root.current = "dashboard"
            app.root.get_screen("dashboard").refresh()
        else:
            MDSnackbar(
                MDSnackbarText(text="Identifiants incorrects"),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                size_hint_x=0.5,
            ).open()


class DashboardScreen(Screen):
    def on_enter(self):
        self.refresh()

    def refresh(self):
        stats = db.get_dashboard_stats()
        self.ids.stat_products.text = str(stats["total_products"])
        self.ids.stat_low_stock.text = str(stats["low_stock"])
        self.ids.stat_customers.text = str(stats["total_customers"])
        self.ids.stat_sales_today.text = f"{stats['sales_today_total']:.2f} €"

        app = MDApp.get_running_app()
        if app.current_user:
            self.ids.user_label.text = app.current_user.get("full_name", "") or app.current_user["username"]

        # Low stock list
        container = self.ids.low_stock_list
        container.clear_widgets()
        low = db.get_low_stock_products()
        if not low:
            container.add_widget(
                MDLabel(
                    text="Aucun produit en stock bas 👍",
                    adaptive_height=True,
                    theme_text_color="Secondary",
                )
            )
        else:
            for p in low[:8]:
                card = MDCard(
                    orientation="horizontal",
                    padding=dp(12),
                    spacing=dp(10),
                    size_hint_y=None,
                    height=dp(56),
                    radius=[dp(8)],
                )
                card.add_widget(
                    MDLabel(
                        text=f"{p['name']} ({p['brand'] or '-'})",
                        adaptive_height=True,
                        pos_hint={"center_y": 0.5},
                    )
                )
                card.add_widget(
                    MDLabel(
                        text=f"Stock: {p['stock']}",
                        adaptive_size=True,
                        theme_text_color="Error",
                        pos_hint={"center_y": 0.5},
                    )
                )
                container.add_widget(card)

    def toggle_menu(self):
        # Simple navigation via snackbar / just go to screens
        pass


class ProductsScreen(Screen):
    def on_enter(self):
        self.refresh()

    def refresh(self):
        self.filter_products(self.ids.search_field.text if "search_field" in self.ids else "")

    def filter_products(self, text):
        products = db.get_all_products(search=text.strip() or None)
        container = self.ids.products_list
        container.clear_widgets()

        if not products:
            container.add_widget(
                MDLabel(text="Aucun produit trouvé", adaptive_height=True, theme_text_color="Secondary")
            )
            return

        for p in products:
            card = MDCard(
                orientation="horizontal",
                padding=dp(12),
                spacing=dp(10),
                size_hint_y=None,
                height=dp(72),
                radius=[dp(10)],
            )
            info = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=dp(2))
            info.add_widget(
                MDLabel(
                    text=f"{p['name']}",
                    font_style="Title",
                    role="small",
                    adaptive_height=True,
                )
            )
            info.add_widget(
                MDLabel(
                    text=f"{p['brand'] or '-'} | {p['category'] or '-'} | Stock: {p['stock']} | {p['price']:.2f} €",
                    font_style="Label",
                    role="medium",
                    theme_text_color="Secondary",
                    adaptive_height=True,
                )
            )
            card.add_widget(info)

            btn_edit = MDIconButton(icon="pencil", on_release=lambda x, pid=p["id"]: self.open_edit_dialog(pid))
            btn_del = MDIconButton(icon="delete", on_release=lambda x, pid=p["id"]: self.confirm_delete(pid))
            card.add_widget(btn_edit)
            card.add_widget(btn_del)
            container.add_widget(card)

    def open_add_dialog(self):
        self._show_product_dialog()

    def open_edit_dialog(self, product_id):
        product = db.get_product(product_id)
        if product:
            self._show_product_dialog(product)

    def _show_product_dialog(self, product=None):
        is_edit = product is not None
        title = "Modifier le produit" if is_edit else "Ajouter un produit"

        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(8),
            size_hint_y=None,
            height=dp(420),
            adaptive_height=False,
        )

        fields = {}
        for key, hint, default in [
            ("name", "Nom du produit *", product["name"] if product else ""),
            ("brand", "Marque", product["brand"] if product else ""),
            ("category", "Catégorie", product["category"] if product else ""),
            ("price", "Prix (€) *", str(product["price"]) if product else ""),
            ("stock", "Stock", str(product["stock"]) if product else "0"),
            ("min_stock", "Stock minimum", str(product["min_stock"]) if product else "5"),
            ("barcode", "Code-barres", product["barcode"] if product and product["barcode"] else ""),
            ("description", "Description", product["description"] if product else ""),
        ]:
            tf = MDTextField(hint_text=hint, mode="outlined", text=str(default or ""))
            fields[key] = tf
            content.add_widget(tf)

        def save(*args):
            name = fields["name"].text.strip()
            if not name:
                MDSnackbar(MDSnackbarText(text="Le nom est obligatoire"), y=dp(24)).open()
                return
            try:
                price = float(fields["price"].text.replace(",", ".") or 0)
                stock = int(fields["stock"].text or 0)
                min_stock = int(fields["min_stock"].text or 5)
            except ValueError:
                MDSnackbar(MDSnackbarText(text="Prix / stock invalides"), y=dp(24)).open()
                return

            brand = fields["brand"].text.strip()
            category = fields["category"].text.strip()
            barcode = fields["barcode"].text.strip() or None
            description = fields["description"].text.strip()

            if is_edit:
                ok = db.update_product(
                    product["id"], name, brand, category, price, stock, min_stock, barcode, description
                )
                if not ok:
                    MDSnackbar(MDSnackbarText(text="Code-barres déjà utilisé"), y=dp(24)).open()
                    return
            else:
                pid = db.add_product(name, brand, category, price, stock, min_stock, barcode, description)
                if pid is None:
                    MDSnackbar(MDSnackbarText(text="Code-barres déjà utilisé"), y=dp(24)).open()
                    return

            dialog.dismiss()
            self.refresh()
            MDSnackbar(MDSnackbarText(text="Produit enregistré"), y=dp(24)).open()

        buttons = MDBoxLayout(adaptive_height=True, spacing=dp(8), padding=[0, dp(8), 0, 0])
        btn_cancel = MDButton(style="text", on_release=lambda x: dialog.dismiss())
        btn_cancel.add_widget(MDButtonText(text="Annuler"))
        btn_save = MDButton(style="filled", on_release=save)
        btn_save.add_widget(MDButtonText(text="Enregistrer"))
        buttons.add_widget(btn_cancel)
        buttons.add_widget(btn_save)

        dialog = MDDialog(
            MDLabel(text=title, font_style="Title", role="medium", adaptive_height=True),
            content,
            buttons,
        )
        dialog.open()

    def confirm_delete(self, product_id):
        product = db.get_product(product_id)
        if not product:
            return

        def do_delete(*args):
            db.delete_product(product_id)
            dialog.dismiss()
            self.refresh()
            MDSnackbar(MDSnackbarText(text="Produit supprimé"), y=dp(24)).open()

        buttons = MDBoxLayout(adaptive_height=True, spacing=dp(8))
        btn_cancel = MDButton(style="text", on_release=lambda x: dialog.dismiss())
        btn_cancel.add_widget(MDButtonText(text="Annuler"))
        btn_del = MDButton(style="filled", on_release=do_delete)
        btn_del.add_widget(MDButtonText(text="Supprimer"))
        buttons.add_widget(btn_cancel)
        buttons.add_widget(btn_del)

        dialog = MDDialog(
            MDLabel(
                text=f"Supprimer « {product['name']} » ?",
                adaptive_height=True,
            ),
            buttons,
        )
        dialog.open()


class SalesScreen(Screen):
    cart = ListProperty([])

    def on_enter(self):
        self.cart = []
        self.update_cart_ui()
        self.search_products("")

    def search_products(self, text):
        products = db.get_all_products(search=text.strip() or None)
        container = self.ids.available_products
        container.clear_widgets()

        for p in products:
            if p["stock"] <= 0:
                continue
            card = MDCard(
                orientation="horizontal",
                padding=dp(10),
                spacing=dp(8),
                size_hint_y=None,
                height=dp(56),
                radius=[dp(8)],
            )
            card.add_widget(
                MDLabel(
                    text=f"{p['name']} — {p['price']:.2f} € (stock: {p['stock']})",
                    adaptive_height=True,
                    pos_hint={"center_y": 0.5},
                )
            )
            btn = MDIconButton(
                icon="plus",
                on_release=lambda x, prod=p: self.add_to_cart(prod),
            )
            card.add_widget(btn)
            container.add_widget(card)

    def add_to_cart(self, product):
        for item in self.cart:
            if item["product_id"] == product["id"]:
                if item["quantity"] < product["stock"]:
                    item["quantity"] += 1
                else:
                    MDSnackbar(MDSnackbarText(text="Stock insuffisant"), y=dp(24)).open()
                self.update_cart_ui()
                return

        self.cart.append(
            {
                "product_id": product["id"],
                "name": product["name"],
                "unit_price": product["price"],
                "quantity": 1,
                "max_stock": product["stock"],
            }
        )
        self.update_cart_ui()

    def update_cart_ui(self):
        container = self.ids.cart_items
        container.clear_widgets()
        total = 0.0

        for item in self.cart:
            subtotal = item["quantity"] * item["unit_price"]
            total += subtotal
            row = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(40),
                spacing=dp(6),
            )
            row.add_widget(
                MDLabel(
                    text=f"{item['name']} x{item['quantity']}",
                    adaptive_height=True,
                    pos_hint={"center_y": 0.5},
                )
            )
            row.add_widget(
                MDLabel(
                    text=f"{subtotal:.2f} €",
                    adaptive_size=True,
                    pos_hint={"center_y": 0.5},
                )
            )
            row.add_widget(
                MDIconButton(
                    icon="minus",
                    on_release=lambda x, pid=item["product_id"]: self.change_qty(pid, -1),
                )
            )
            row.add_widget(
                MDIconButton(
                    icon="plus",
                    on_release=lambda x, pid=item["product_id"]: self.change_qty(pid, 1),
                )
            )
            container.add_widget(row)

        self.ids.cart_total.text = f"Total : {total:.2f} €"

    def change_qty(self, product_id, delta):
        for item in self.cart:
            if item["product_id"] == product_id:
                new_qty = item["quantity"] + delta
                if new_qty <= 0:
                    self.cart = [i for i in self.cart if i["product_id"] != product_id]
                elif new_qty > item["max_stock"]:
                    MDSnackbar(MDSnackbarText(text="Stock insuffisant"), y=dp(24)).open()
                else:
                    item["quantity"] = new_qty
                break
        self.update_cart_ui()

    def clear_cart(self):
        self.cart = []
        self.update_cart_ui()

    def checkout(self):
        if not self.cart:
            MDSnackbar(MDSnackbarText(text="Le panier est vide"), y=dp(24)).open()
            return

        app = MDApp.get_running_app()
        items = [
            {
                "product_id": i["product_id"],
                "quantity": i["quantity"],
                "unit_price": i["unit_price"],
            }
            for i in self.cart
        ]
        try:
            sale_id = db.create_sale(
                customer_id=None,
                user_id=app.current_user["id"],
                items=items,
                payment_method="espèces",
            )
            self.clear_cart()
            MDSnackbar(
                MDSnackbarText(text=f"Vente #{sale_id} enregistrée avec succès !"),
                y=dp(24),
            ).open()
            # Refresh product list (stock changed)
            self.search_products(self.ids.product_search.text)
        except Exception as e:
            MDSnackbar(MDSnackbarText(text=f"Erreur: {e}"), y=dp(24)).open()


class CustomersScreen(Screen):
    def on_enter(self):
        self.refresh()

    def refresh(self):
        self.filter_customers(self.ids.search_field.text if "search_field" in self.ids else "")

    def filter_customers(self, text):
        customers = db.get_all_customers(search=text.strip() or None)
        container = self.ids.customers_list
        container.clear_widgets()

        if not customers:
            container.add_widget(
                MDLabel(text="Aucun client", adaptive_height=True, theme_text_color="Secondary")
            )
            return

        for c in customers:
            card = MDCard(
                orientation="horizontal",
                padding=dp(12),
                spacing=dp(10),
                size_hint_y=None,
                height=dp(64),
                radius=[dp(10)],
            )
            info = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=dp(2))
            info.add_widget(
                MDLabel(text=c["name"], font_style="Title", role="small", adaptive_height=True)
            )
            info.add_widget(
                MDLabel(
                    text=f"{c['phone'] or ''}  {c['email'] or ''}",
                    font_style="Label",
                    role="medium",
                    theme_text_color="Secondary",
                    adaptive_height=True,
                )
            )
            card.add_widget(info)
            card.add_widget(
                MDIconButton(icon="pencil", on_release=lambda x, cid=c["id"]: self.open_edit_dialog(cid))
            )
            card.add_widget(
                MDIconButton(icon="delete", on_release=lambda x, cid=c["id"]: self.confirm_delete(cid))
            )
            container.add_widget(card)

    def open_add_dialog(self):
        self._show_customer_dialog()

    def open_edit_dialog(self, customer_id):
        customers = db.get_all_customers()
        customer = next((c for c in customers if c["id"] == customer_id), None)
        if customer:
            self._show_customer_dialog(customer)

    def _show_customer_dialog(self, customer=None):
        is_edit = customer is not None
        title = "Modifier le client" if is_edit else "Nouveau client"

        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(8),
            size_hint_y=None,
            height=dp(260),
        )
        fields = {}
        for key, hint, default in [
            ("name", "Nom complet *", customer["name"] if customer else ""),
            ("phone", "Téléphone", customer["phone"] if customer else ""),
            ("email", "Email", customer["email"] if customer else ""),
            ("address", "Adresse", customer["address"] if customer else ""),
        ]:
            tf = MDTextField(hint_text=hint, mode="outlined", text=str(default or ""))
            fields[key] = tf
            content.add_widget(tf)

        def save(*args):
            name = fields["name"].text.strip()
            if not name:
                MDSnackbar(MDSnackbarText(text="Le nom est obligatoire"), y=dp(24)).open()
                return
            if is_edit:
                db.update_customer(
                    customer["id"],
                    name,
                    fields["phone"].text.strip(),
                    fields["email"].text.strip(),
                    fields["address"].text.strip(),
                )
            else:
                db.add_customer(
                    name,
                    fields["phone"].text.strip(),
                    fields["email"].text.strip(),
                    fields["address"].text.strip(),
                )
            dialog.dismiss()
            self.refresh()
            MDSnackbar(MDSnackbarText(text="Client enregistré"), y=dp(24)).open()

        buttons = MDBoxLayout(adaptive_height=True, spacing=dp(8))
        btn_cancel = MDButton(style="text", on_release=lambda x: dialog.dismiss())
        btn_cancel.add_widget(MDButtonText(text="Annuler"))
        btn_save = MDButton(style="filled", on_release=save)
        btn_save.add_widget(MDButtonText(text="Enregistrer"))
        buttons.add_widget(btn_cancel)
        buttons.add_widget(btn_save)

        dialog = MDDialog(
            MDLabel(text=title, font_style="Title", role="medium", adaptive_height=True),
            content,
            buttons,
        )
        dialog.open()

    def confirm_delete(self, customer_id):
        def do_delete(*args):
            db.delete_customer(customer_id)
            dialog.dismiss()
            self.refresh()
            MDSnackbar(MDSnackbarText(text="Client supprimé"), y=dp(24)).open()

        buttons = MDBoxLayout(adaptive_height=True, spacing=dp(8))
        btn_cancel = MDButton(style="text", on_release=lambda x: dialog.dismiss())
        btn_cancel.add_widget(MDButtonText(text="Annuler"))
        btn_del = MDButton(style="filled", on_release=do_delete)
        btn_del.add_widget(MDButtonText(text="Supprimer"))
        buttons.add_widget(btn_cancel)
        buttons.add_widget(btn_del)

        dialog = MDDialog(
            MDLabel(text="Supprimer ce client ?", adaptive_height=True),
            buttons,
        )
        dialog.open()


class HistoryScreen(Screen):
    def on_enter(self):
        self.refresh()

    def refresh(self):
        sales = db.get_sales(limit=100)
        container = self.ids.sales_list
        container.clear_widgets()

        if not sales:
            container.add_widget(
                MDLabel(text="Aucune vente enregistrée", adaptive_height=True, theme_text_color="Secondary")
            )
            return

        for s in sales:
            date_str = s["created_at"][:16].replace("T", " ") if s["created_at"] else ""
            card = MDCard(
                orientation="vertical",
                padding=dp(12),
                spacing=dp(4),
                size_hint_y=None,
                height=dp(80),
                radius=[dp(10)],
            )
            card.add_widget(
                MDLabel(
                    text=f"Vente #{s['id']} — {s['total']:.2f} €",
                    font_style="Title",
                    role="small",
                    adaptive_height=True,
                )
            )
            card.add_widget(
                MDLabel(
                    text=f"{date_str}  |  {s['payment_method'] or 'espèces'}  |  Vendeur: {s['seller_name'] or '-'}",
                    font_style="Label",
                    role="medium",
                    theme_text_color="Secondary",
                    adaptive_height=True,
                )
            )
            container.add_widget(card)


class BoutiqueApp(MDApp):
    current_user = ObjectProperty(None, allownone=True)

    def build(self):
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.theme_style = "Light"
        self.title = "Boutique Cosmétique"

        db.init_db()

        Builder.load_string(KV)

        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(ProductsScreen(name="products"))
        sm.add_widget(SalesScreen(name="sales"))
        sm.add_widget(CustomersScreen(name="customers"))
        sm.add_widget(HistoryScreen(name="history"))
        return sm

    def go_to(self, screen_name):
        self.root.transition = SlideTransition(direction="left")
        self.root.current = screen_name

    def logout(self):
        self.current_user = None
        self.root.transition = SlideTransition(direction="right")
        self.root.current = "login"


if __name__ == "__main__":
    BoutiqueApp().run()
