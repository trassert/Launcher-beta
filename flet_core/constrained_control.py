from typing import Any, Optional, Union
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalEventCallable,
)
class ConstrainedControl(Control):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        rtl: Optional[bool] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end: OptionalEventCallable = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
            rtl=rtl,
        )
        self.key = key
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.scale = scale
        self.rotate = rotate
        self.offset = offset
        self.aspect_ratio = aspect_ratio
        self.animate_opacity = animate_opacity
        self.animate_size = animate_size
        self.animate_position = animate_position
        self.animate_rotation = animate_rotation
        self.animate_scale = animate_scale
        self.animate_offset = animate_offset
        self.on_animation_end = on_animation_end
    def before_update(self):
        super().before_update()
        self._set_attr_json("rotate", self.__rotate)
        self._set_attr_json("scale", self.__scale)
        self._set_attr_json("offset", self.__offset)
        self._set_attr_json("animateOpacity", self.__animate_opacity)
        self._set_attr_json("animateSize", self.__animate_size)
        self._set_attr_json("animatePosition", self.__animate_position)
        self._set_attr_json("animateRotation", self.__animate_rotation)
        self._set_attr_json("animateScale", self.__animate_scale)
        self._set_attr_json("animateOffset", self.__animate_offset)
    @property
    def key(self) -> Optional[str]:
        return self._get_attr("key")
    @key.setter
    def key(self, value: Optional[str]):
        self._set_attr("key", value)
    @property
    def width(self) -> OptionalNumber:
        """
        Control width.
        """
        return self._get_attr("width")
    @width.setter
    def width(self, value: OptionalNumber):
        self._set_attr("width", value)
    @property
    def height(self) -> OptionalNumber:
        return self._get_attr("height")
    @height.setter
    def height(self, value: OptionalNumber):
        self._set_attr("height", value)
    @property
    def left(self) -> OptionalNumber:
        return self._get_attr("left")
    @left.setter
    def left(self, value: OptionalNumber):
        self._set_attr("left", value)
    @property
    def top(self) -> OptionalNumber:
        return self._get_attr("top")
    @top.setter
    def top(self, value: OptionalNumber):
        self._set_attr("top", value)
    @property
    def right(self) -> OptionalNumber:
        return self._get_attr("right")
    @right.setter
    def right(self, value: OptionalNumber):
        self._set_attr("right", value)
    @property
    def bottom(self) -> OptionalNumber:
        return self._get_attr("bottom")
    @bottom.setter
    def bottom(self, value: OptionalNumber):
        self._set_attr("bottom", value)
    @property
    def rotate(self) -> RotateValue:
        return self.__rotate
    @rotate.setter
    def rotate(self, value: RotateValue):
        self.__rotate = value
    @property
    def scale(self) -> ScaleValue:
        return self.__scale
    @scale.setter
    def scale(self, value: ScaleValue):
        self.__scale = value
    @property
    def offset(self) -> OffsetValue:
        return self.__offset
    @offset.setter
    def offset(self, value: OffsetValue):
        self.__offset = value
    @property
    def aspect_ratio(self) -> OptionalNumber:
        return self._get_attr("aspectRatio")
    @aspect_ratio.setter
    def aspect_ratio(self, value: OptionalNumber):
        self._set_attr("aspectRatio", value)
    @property
    def animate_opacity(self) -> AnimationValue:
        return self.__animate_opacity
    @animate_opacity.setter
    def animate_opacity(self, value: AnimationValue):
        self.__animate_opacity = value
    @property
    def animate_size(self) -> AnimationValue:
        return self.__animate_size
    @animate_size.setter
    def animate_size(self, value: AnimationValue):
        self.__animate_size = value
    @property
    def animate_position(self) -> AnimationValue:
        return self.__animate_position
    @animate_position.setter
    def animate_position(self, value: AnimationValue):
        self.__animate_position = value
    @property
    def animate_rotation(self) -> AnimationValue:
        return self.__animate_rotation
    @animate_rotation.setter
    def animate_rotation(self, value: AnimationValue):
        self.__animate_rotation = value
    @property
    def animate_scale(self) -> AnimationValue:
        return self.__animate_scale
    @animate_scale.setter
    def animate_scale(self, value: AnimationValue):
        self.__animate_scale = value
    @property
    def animate_offset(self) -> AnimationValue:
        return self.__animate_offset
    @animate_offset.setter
    def animate_offset(self, value: AnimationValue):
        self.__animate_offset = value
    @property
    def on_animation_end(self) -> OptionalEventCallable:
        return self._get_event_handler("animation_end")
    @on_animation_end.setter
    def on_animation_end(self, handler: OptionalEventCallable):
        self._add_event_handler("animation_end", handler)
        self._set_attr("onAnimationEnd", True if handler is not None else None)
