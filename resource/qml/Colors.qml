// Copyright (C) 2023 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import QtQuick

pragma Singleton

QtObject {
    // 主色调
    property color primary: "#1296db"
    property color primary90: "#1a8fd1"
    property color primary80: "#2188c7"
    property color primary70: "#2981bd"
    property color primary60: "#307ab3"
    
    // 背景色
    property color darkest: "#1e293b"
    property color darker: "#334155"
    property color dark: "#475569"
    property color lightGray: "#f1f5f9"
    property color light: "#f8fafc"
    property color white: "#ffffff"
    
    // 辅助色
    property color secondary: "#0d6efd"
    property color accent: "#36c2cf"
    property color success: "#10b981"
    property color warning: "#f59e0b"
    property color danger: "#ef4444"
    property color info: "#06b6d4"
    
    // 中性色
    property color midGray: "#e3e8ee"
    property color darkGray: "#d9d9d9"
    
    // 文本色
    property color textOnDark: "#ffffff"
    property color textOnLight: "#475569"
    property color bodyText: "#64748b"
    
    // 阴影色
    // property color shadow: "rgba(0, 0, 0, 0.15)"
}
