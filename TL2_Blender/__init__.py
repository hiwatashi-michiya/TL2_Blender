import bpy

# ブレンダーに登録するアドオン情報
bl_info = {
    "name": "レベルエディタ",
    "author": "Michiya Hiwatashi",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "",
    "description": "レベルエディタ",
    "warning": "",
    #"support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

# モジュールのインポート

from .add_collider import MYADDON_OT_add_collider
from .add_filename import MYADDON_OT_add_filename
from .collider import OBJECT_PT_collider
from .create_ico_sphere import MYADDON_OT_create_ico_sphere
from .draw_collider import DrawCollider
from .export_scene import MYADDON_OT_export_scene
from .file_name import OBJECT_PT_file_name
from .stretch_vertex import MYADDON_OT_stretch_vertex

#メニュー項目描画
def draw_menu_manual(self, context):
    #self : 呼び出し元のクラスインスタンス。C++におけるthisポインタ
    #context : カーソルを合わせたときのポップアップのカスタマイズ等に使用

    #トップバーの「エディターメニュー」に項目(オペレータ)を追加
    self.layout.operator("wm.url_open_preset", text="Manual", icon='HELP')

#トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):

    #Blenderがクラスを識別するための固有の文字列
    bl_idname = "TOPBAR_MT_my_menu"
    #メニューのラベルとして表示される文字列
    bl_label = "MyMenu"
    #著者表示用の文字列
    bl_description = "拡張メニュー by " + bl_info["author"]

    #サブメニューの描画
    def draw(self, context):

        #トップバーの「エディターメニュー」に項目(オペレータ)を追加
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname,
            text=MYADDON_OT_stretch_vertex.bl_label)
        self.layout.separator()
        self.layout.operator(MYADDON_OT_create_ico_sphere.bl_idname,
            text=MYADDON_OT_create_ico_sphere.bl_label)
        self.layout.separator()
        self.layout.operator(MYADDON_OT_export_scene.bl_idname,
            text=MYADDON_OT_export_scene.bl_label)

    #既存のメニューにサブメニューを追加
    def submenu(self, context):

        # ID指定でサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)

#Blenderに登録するクラスリスト
classes = (
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    MYADDON_OT_add_filename,
    MYADDON_OT_add_collider,
    TOPBAR_MT_my_menu,
    OBJECT_PT_file_name,
    OBJECT_PT_collider,
)

#アドオン有効化時コールバック
def register():
    #Blenderにクラスを登録
    for cls in classes:
        bpy.utils.register_class(cls)

    #メニューに項目を追加
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    #3Dビューに描画関数を追加
    DrawCollider.handle = bpy.types.SpaceView3D.draw_handler_add(DrawCollider.draw_collider, (), "WINDOW", "POST_VIEW")
    print("レベルエディタが有効化されました。")

#アドオン無効化時コールバック
def unregister():
     #メニューから項目を削除
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)
    #3Dビューから描画関数を削除
    bpy.types.SpaceView3D.draw_handler_remove(DrawCollider.handle, "WINDOW")
    print("レベルエディタが無効化されました。")

    #Blenderからクラスを削除
    for cls in classes:
        bpy.utils.unregister_class(cls)
    

#テスト実行用コード
if __name__ == "__main__":
    register()