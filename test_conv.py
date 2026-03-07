import tempfile
import unittest
from pathlib import Path

from PIL import Image

import conv


class ConvertImageTests(unittest.TestCase):
    def test_convert_png_to_gif(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "sample.png"
            Image.new("RGBA", (8, 8), (255, 0, 0, 128)).save(input_path, format="PNG")

            output_path = conv.convert_image(input_path, "gif")

            self.assertEqual(output_path.suffix, ".gif")
            self.assertTrue(output_path.exists())

            with Image.open(output_path) as out:
                self.assertEqual(out.format, "GIF")
                self.assertEqual(out.size, (8, 8))

    def test_prepare_output_image_preserves_animation_for_gif_and_webp(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "animated.gif"
            frames = [
                Image.new("RGBA", (6, 6), (255, 0, 0, 255)),
                Image.new("RGBA", (6, 6), (0, 255, 0, 255)),
            ]
            frames[0].save(
                input_path,
                format="GIF",
                save_all=True,
                append_images=frames[1:],
                duration=80,
                loop=0,
            )

            with Image.open(input_path) as animated:
                gif_first, gif_kwargs = conv.prepare_output_image(animated, "gif")
                self.assertTrue(gif_kwargs["save_all"])
                self.assertEqual(len(gif_kwargs["append_images"]), 1)
                self.assertEqual(gif_kwargs["duration"], 80)
                self.assertEqual(gif_kwargs["loop"], 0)
                self.assertEqual(gif_first.size, (6, 6))

            with Image.open(input_path) as animated:
                webp_first, webp_kwargs = conv.prepare_output_image(animated, "webp")
                self.assertTrue(webp_kwargs["save_all"])
                self.assertEqual(len(webp_kwargs["append_images"]), 1)
                self.assertEqual(webp_kwargs["duration"], 80)
                self.assertEqual(webp_kwargs["loop"], 0)
                self.assertEqual(webp_first.size, (6, 6))


if __name__ == "__main__":
    unittest.main()
