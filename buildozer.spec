[app]

title = Cosmetic Shop
package.name = cosmeticshop
package.domain = org.nexorahub

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,json,atlas,ttf,txt,db

version = 1.0

requirements = python3,kivy,kivymd

orientation = portrait

fullscreen = 0

android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True

[buildozer]

log_level = 2
warn_on_root = 1
