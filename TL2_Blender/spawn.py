import bpy
import bpy.ops
import os

class SpawnNames():

    # インデックス
    PROTOTYPE = 0 #プロトタイプのオブジェクト名
    INSTANCE = 1 # 量産時のオブジェクト名
    FILENAME = 2 # リソースファイル名

    names = {}
    # names["キー"] = (プロトタイプのオブジェクト名、量産時のオブジェクト名、リソースファイル名)
    names["Enemy"] = ("PrototypeEnemySpawn", "EnemySpawn", "bucket/bucket.obj")
    names["Player"] = ("PrototypePlayerSpawn", "PlayerSpawn", "ghostBox/ghostBox.obj")



#オペレータ 出現ポイントのシンボルを読み込む
class MYADDON_OT_import_spawnpoint(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_import_spawnpoint"
    bl_label = "出現ポイントシンボルimport"
    bl_description = "出現ポイントのシンボルをImportします"
    prototype_object_name = "PrototypePlayerSpawn"
    object_name = "PlayerSpawn"

    def execute(self, context):
        # Enemyオブジェクト読み込み
        self.load_obj("Enemy")
        # Playerオブジェクト読み込み
        self.load_obj("Player")

        return {"FINISHED"}

    def load_obj(self, type):
        print("出現ポイントのシンボルをImportします")
        # 重複ロード防止
        spawn_object = bpy.data.objects.get(SpawnNames.names[type][SpawnNames.PROTOTYPE])
        if spawn_object is not None:
            return {'CANCELLED'}
        # スクリプトが配置されているディレクトリの名前を取得する
        addon_directory = os.path.dirname(__file__)
        # ディレクトリからのモデルファイルの相対パスを記述
        relative_path = SpawnNames.names[type][SpawnNames.FILENAME]
        # 合成してモデルファイルのフルパスを得る
        full_path = os.path.join(addon_directory, relative_path)
        # オブジェクトをインポート
        bpy.ops.wm.obj_import('EXEC_DEFAULT',
            filepath=full_path, display_type='THUMBNAIL',
            forward_axis='Z', up_axis='Y')
        # 回転を適用
        bpy.ops.object.transform_apply(location=False,
            rotation=True, scale=False, properties=False,
            isolate_users=False)
        # アクティブなオブジェクトを取得
        object = bpy.context.active_object
        # オブジェクト名を変更
        object.name = SpawnNames.names[type][SpawnNames.PROTOTYPE]
        # オブジェクトの種類を設定
        object["type"] = SpawnNames.names[type][SpawnNames.INSTANCE]
        # メモリ上には置いておくがシーンから外す
        bpy.context.collection.objects.unlink(object)

        return {"FINISHED"}

#オペレータ 出現ポイントのシンボルを作成・配置する
class MYADDON_OT_create_spawnpoint(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_spawnpoint"
    bl_label = "出現ポイントシンボルの作成"
    bl_description = "出現ポイントのシンボルを作成します"
    bl_options = {"REGISTER", "UNDO"}

    # プロパティ（引数として渡せる）
    type: bpy.props.StringProperty(name="Type", default="Player")

    def execute(self, context):
        # 読み込み済みのコピー元オブジェクトを検索
        spawn_object = bpy.data.objects.get(SpawnNames.names[self.type][SpawnNames.PROTOTYPE])

        # まだ読み込んでいない場合
        if spawn_object is None:
            #読み込みオペレータを実行する
            bpy.ops.myaddon.myaddon_ot_import_spawnpoint('EXEC_DEFAULT')
            # 再検索
            spawn_object = bpy.data.objects.get(SpawnNames.names[self.type][SpawnNames.PROTOTYPE])
        
        print("出現ポイントのシンボルを作成します")

        # Blenderでの選択を解除する
        bpy.ops.object.select_all(action='DESELECT')

        # 複製元の非表示オブジェクトを複製する
        object = spawn_object.copy()

        # 複製したオブジェクトを現在のシーンにリンク（出現させる）
        bpy.context.collection.objects.link(object)

        # オブジェクト名を変更
        object.name = SpawnNames.names[self.type][SpawnNames.INSTANCE]

        return {"FINISHED"}

class MYADDON_OT_create_playerspawnpoint(bpy.types.Operator):

    bl_idname = "myaddon.myaddon_ot_create_playerspawnpoint"
    bl_label = "プレイヤー出現ポイントシンボルの作成"
    bl_description = "プレイヤー出現ポイントのシンボルを作成します"

    def execute(self, context):

        bpy.ops.myaddon.myaddon_ot_create_spawnpoint('EXEC_DEFAULT', type = "Player")

        return {'FINISHED'}

class MYADDON_OT_create_enemyspawnpoint(bpy.types.Operator):

    bl_idname = "myaddon.myaddon_ot_create_enemyspawnpoint"
    bl_label = "敵出現ポイントシンボルの作成"
    bl_description = "敵出現ポイントのシンボルを作成します"

    def execute(self, context):

        bpy.ops.myaddon.myaddon_ot_create_spawnpoint('EXEC_DEFAULT', type = "Enemy")

        return {'FINISHED'}    


