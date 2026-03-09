[app]

title = Taxi Calculator
package.name = taxicalc
package.domain = org.taxicalc

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

# Android configuration
android.api = 33
android.sdk = 33
android.minapi = 21

android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

android.build_tools_version = 34.0.0
