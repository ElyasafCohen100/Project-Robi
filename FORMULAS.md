# 🤖 Project ROBI — The Formula Book

> 🧙‍♂️ **Swaggy Robotics Academy** · A simple, visual guide to the math behind ROBI.
>
> **Our goal:** Understand each formula, know when to use it, and find its Python function quickly.

---

## 🗺️ Quick Navigation

| Chapter | What we learn |
|:--|:--|
| [🧭 1. Geometry & Navigation](#-1-geometry--navigation) | Move, find targets, and work with angles |
| [🛞 2. Differential Drive](#-2-differential-drive) | Turn wheel speeds into robot speeds |
| [⏱️ 3. Motion Over Time](#️-3-motion-over-time) | Update position as time passes |
| [📡 4. Encoders & Odometry](#-4-encoders--odometry) | Estimate motion using wheel measurements |
| [🔎 Python Function Map](#-python-function-map) | Find the code behind each formula |

### 🎨 How to read this book

- ✅ **In code** — We already use this formula in Project ROBI.
- 🧪 **Next to build** — We learned the formula but have not implemented it yet.
- 📍 **Pose** — `Pose2D(x, y, theta)` stores the robot's position and heading.

**Our units:** distance = meters (`m`), time = seconds (`s`), speed = `m/s`, angles = radians (`rad`), angular speed = `rad/s`.

**Our map:** +X → right, +Y ↑ up, positive rotation ↶ counterclockwise. `Pose2D.theta` is stored in **radians**.

---

## 🧭 1. Geometry & Navigation

*How can ROBI move in a direction or find a target?*

### 1.1 ↗️ Move in a direction · ✅ In code

**What does it do?** Splits one move into an X part and a Y part.

$$
\boxed{\Delta x = d\cos(\theta)}
$$

$$
\boxed{\Delta y = d\sin(\theta)}
$$

| Symbol | Simple meaning |
|:--|:--|
| $d$ | How far ROBI moves (m); can be negative |
| $\theta$ | Direction ROBI faces (rad) |
| $\Delta x,\ \Delta y$ | How much X and Y change (m) |

**🧮 Example:** Move `1 m` at `45°` → X increases by about `0.71 m`, and Y increases by about `0.71 m`.

**🐍 Python:** `Robot.move()` → `robi/robot.py`

### 1.2 📏 Distance to a target · ✅ In code

**What does it do?** Finds the straight-line distance from ROBI to a target point.

$$
\Delta x = x_{\mathrm{target}} - x
$$

$$
\Delta y = y_{\mathrm{target}} - y
$$

$$
\boxed{d = \sqrt{(\Delta x)^2 + (\Delta y)^2}}
$$

**🧮 Example:** Target is `(3, 4)`, ROBI is at `(0, 0)` → distance = `5 m`.

**🐍 Python:** `math.hypot(delta_x, delta_y)` inside `Robot.move_to()` → `robi/robot.py`

### 1.3 🎯 Direction to a target · ✅ In code

**What does it do?** Finds the angle ROBI should face to look at a target.

$$
\boxed{\theta_{\mathrm{target}} = \operatorname{atan2}(\Delta y,\Delta x)}
$$

**💡 Remember:** `atan2` takes **Y first, X second**. It returns radians.

**🐍 Python:** `math.atan2(delta_y, delta_x)` inside `Robot.move_to()` → `robi/robot.py`. `Robot.rotate_to()` accepts degrees, so the result is converted before calling it.

### 1.4 🔄 Shortest turn to an angle · ✅ In code

**What does it do?** Finds the shortest signed turn from one heading to another.

$$
\boxed{\Delta\theta = (\theta_{\mathrm{target}}-\theta_{\mathrm{current}}+\pi)\bmod 2\pi-\pi}
$$

**🧮 Example:** From `350°` to `10°` → turn **+20°**, not −340°.

**💡 Remember:** Result is between `−π` (included) and `π` (not included).

**🐍 Python:** `shortest_angular_distance()` → `robi/geometry.py`; used by `Robot.rotate_to()`.

### 1.5 🧭 Keep an angle in range · ✅ In code

**What does it do?** Keeps a heading between `0` and `2π` radians.

$$
\boxed{\theta_{\mathrm{new}}=\theta\bmod 2\pi}
$$

**🧮 Example:** `370°` becomes `10°`.

**🐍 Python:** `% math.tau` in `Robot.rotate()` and `Robot.drive()` → `robi/robot.py`.

### 1.6 🔁 Degrees ↔ radians · ✅ In code

**What does it do?** Converts human-friendly degrees to radians and back.

$$
\boxed{\theta_{\mathrm{rad}}=\theta_{\mathrm{deg}}\frac{\pi}{180}}
$$

$$
\boxed{\theta_{\mathrm{deg}}=\theta_{\mathrm{rad}}\frac{180}{\pi}}
$$

**🧮 Example:** `180° = π rad`.

**🐍 Python:** `math.radians()` and `math.degrees()`.

---

## 🛞 2. Differential Drive

*ROBI has two driven wheels. The difference between their speeds makes ROBI turn.*

### 2.1 ➡️ Robot forward speed · ✅ In code

**What does it do?** Finds the forward speed of the robot's center.

$$
\boxed{v=\frac{v_L+v_R}{2}}
$$

| Symbol | Simple meaning |
|:--|:--|
| $v_L$ | Left wheel speed (m/s) |
| $v_R$ | Right wheel speed (m/s) |
| $v$ | Robot center speed (m/s) |

**🧮 Example:** Left = `1 m/s`, right = `2 m/s` → center speed = `1.5 m/s`.

**🐍 Python:** `calculate_linear_velocity()` → `robi/differential_drive.py`

### 2.2 ↶ How fast ROBI turns · ✅ In code

**What does it do?** Finds the robot's turning speed.

$$
\boxed{\omega=\frac{v_R-v_L}{L}}
$$

| Symbol | Simple meaning |
|:--|:--|
| $\omega$ | Turning speed (rad/s) |
| $L$ | Distance **between** the wheels (m) |

**🧮 Example:** Left = `1 m/s`, right = `2 m/s`, `L = 0.5 m` → `ω = 2 rad/s`.

**💡 Remember:** Right wheel faster → turn left. `L` must be greater than zero. In code, `L` is called `wheel_separation`.

**🐍 Python:** `calculate_angular_velocity()` → `robi/differential_drive.py`

---

## ⏱️ 3. Motion Over Time

*How do we update ROBI's position after a short time step?*

### 3.1 🏃 Position change in one step · ✅ In code

**What does it do?** Estimates how far ROBI moves along X and Y in a short time.

$$
\boxed{\Delta x=v\cos(\theta)\Delta t}
$$

$$
\boxed{\Delta y=v\sin(\theta)\Delta t}
$$

**Symbols:** `v` = forward speed (`m/s`); `θ` = heading (`rad`); `Δt` = step duration (`s`).

**🧮 Example:** Move at `1 m/s` for `2 s`, facing `0°` → `Δx = 2 m`, `Δy = 0 m`.

**🐍 Python:** `calculate_displacement()` → `robi/geometry.py`. `delta_t` cannot be negative.

### 3.2 🧭 Heading change in one step · ✅ In code

**What does it do?** Updates the direction ROBI faces.

$$
\boxed{\Delta\theta=\omega\Delta t}
$$

$$
\boxed{\theta_{\mathrm{new}}=(\theta_{\mathrm{old}}+\Delta\theta)\bmod 2\pi}
$$

**🧮 Example:** Turn at `1 rad/s` for `2 s` → heading changes by `2 rad`.

**🐍 Python:** `Robot.drive()` → `robi/robot.py`

### 3.3 📍 Update X and Y (Euler method) · ✅ In code

**What does it do?** Adds the movement to ROBI's old position.

$$
\boxed{x_{\mathrm{new}}=x_{\mathrm{old}}+v\cos(\theta_{\mathrm{old}})\Delta t}
$$

$$
\boxed{y_{\mathrm{new}}=y_{\mathrm{old}}+v\sin(\theta_{\mathrm{old}})\Delta t}
$$

**💡 Important:** This method uses the **starting heading** for the whole step. When ROBI turns during the step, this is an approximation. Shorter steps usually help.

**🐍 Python:** `Robot.drive()` → `robi/robot.py`

**🔗 Also used by:** `Robot.drive_wheels()` converts wheel speeds into `v` and `ω`, then calls `drive()`. Right now these are **given speeds**, not encoder measurements.

---

## 📡 4. Encoders & Odometry

> **Wheel Encoder:** Measures wheel or motor-shaft rotation, often by counting pulses.
>
> **Odometry:** Uses measured motion to **estimate** where ROBI moved. It is not perfect: wheel slip can cause errors.

### 4.1 🔢 Pulses → wheel turns · 🧪 Next to build

**What does it do?** Converts encoder pulses into full wheel rotations.

$$
\boxed{N_{\mathrm{rot}}=\frac{N_{\mathrm{pulses}}}{PPR}}
$$

**Symbols:** `PPR` = counted pulses per **wheel** revolution; `N_pulses` = measured pulses.

**🧮 Example:** `30 pulses / 10 pulses per turn = 3 turns`.

**💡 Important:** Real encoders may count edges differently. If the encoder measures the motor shaft, we may also need the gearbox ratio.

**🐍 Python:** Encoder conversion helper — **not built yet**.

### 4.2 ⭕ Wheel circumference · 🧪 Next to build

**What does it do?** Finds how far a wheel rolls in one full turn (without slipping).

$$
\boxed{C=\pi D=2\pi r}
$$

**Symbols:** `C` = circumference (m); `D` = diameter (m); `r` = radius (m).

**🧮 Example:** Diameter = `0.20 m` → circumference ≈ `0.628 m`.

**🐍 Python:** Wheel measurement helper — **not built yet**.

### 4.3 🛞 Pulses → traveled distance · 🧪 Next to build

**What does it do?** Estimates how far **one wheel** rolled.

$$
\boxed{d_{\mathrm{wheel}}=\frac{N_{\mathrm{pulses}}}{PPR}\pi D}
$$

**🧮 Example:** `50 pulses`, `20 pulses/turn`, diameter `0.20 m`:

$$
\frac{50}{20}\times\pi\times0.20\approx\boxed{1.571\ \mathrm{m}}
$$

**💡 Remember:** This measures wheel rotation, **not guaranteed robot travel** if the wheel slips.

**🐍 Python:** Pulse-to-distance helper — **not built yet**.

### 4.4 🤖 Distance of ROBI's center · ✅ In code

**What does it do?** Finds the distance the robot center traveled **along its path**.

$$
\boxed{\Delta s=\frac{d_L+d_R}{2}}
$$

**Symbols:** `d_L` = left wheel travel (m); `d_R` = right wheel travel (m). Both can be negative when moving backward.

**🧮 Example:** Left = `1 m`, right = `2 m` → center path distance = `1.5 m`.

**🐍 Python:** `calculate_center_distance()` → `robi/differential_drive.py`

### 4.5 ↶ Heading change from wheel distances · 🧪 Next to build

**What does it do?** Finds how much ROBI turned from the **difference in wheel distances**.

$$
\boxed{\Delta\theta=\frac{d_R-d_L}{L}}
$$

**🧮 Example:** Left = `1 m`, right = `1.2 m`, `L = 0.5 m` → turn = `0.4 rad` (left).

**💡 Remember:** `d_L` and `d_R` are distances each wheel traveled. `L` is the physical distance **between** the wheels. They are not the same thing!

**🐍 Python:** Distance-based heading helper — **not built yet**. The related speed formula is already in `calculate_angular_velocity()`.

### 4.6 🎯 Midpoint heading · 🧪 Next to build

**What does it do?** Gives a better estimate of X and Y when ROBI moves and turns at the same time.

$$
\boxed{\theta_{\mathrm{mid}}=\theta_{\mathrm{old}}+\frac{\Delta\theta}{2}}
$$

$$
\boxed{\Delta x\approx\Delta s\cos(\theta_{\mathrm{mid}})}
$$

$$
\boxed{\Delta y\approx\Delta s\sin(\theta_{\mathrm{mid}})}
$$

**🧮 Example:** Start heading = `0°`, turn = `60°` → midpoint heading = `30°`.

**💡 Important:** This is still an **approximation**, especially for a large turn in one step.

**🐍 Python:** Odometry pose estimator — **not built yet**.

### 4.7 📍 Update the estimated pose · 🧪 Next to build

**What does it do?** Adds the measured movement to our **estimated** position.

$$
\boxed{x_{\mathrm{new}}=x_{\mathrm{old}}+\Delta x}
$$

$$
\boxed{y_{\mathrm{new}}=y_{\mathrm{old}}+\Delta y}
$$

$$
\boxed{\theta_{\mathrm{new}}=(\theta_{\mathrm{old}}+\Delta\theta)\bmod2\pi}
$$

**💡 Remember:** The estimated pose may drift away from the true pose. Our current `Robot.drive()` changes a **simulated** pose; it does not yet keep a separate estimate based on encoder data.

**🐍 Python:** Odometry pose estimator — **not built yet**.

---

## 🔎 Python Function Map

*Looking at a Python function and wondering which formula it uses? Start here.*

| Python function | File | Formula | Progress |
|:--|:--|:--|:--:|
| `Robot.move()` | `robi/robot.py` | 1.1 | ✅ |
| `Robot.move_to()` | `robi/robot.py` | 1.2, 1.3 | ✅ |
| `shortest_angular_distance()` | `robi/geometry.py` | 1.4 | ✅ |
| `Robot.rotate()` / `Robot.rotate_to()` | `robi/robot.py` | 1.4–1.6 | ✅ |
| `calculate_linear_velocity()` | `robi/differential_drive.py` | 2.1 | ✅ |
| `calculate_angular_velocity()` | `robi/differential_drive.py` | 2.2 | ✅ |
| `calculate_displacement()` | `robi/geometry.py` | 3.1 | ✅ |
| `Robot.drive()` | `robi/robot.py` | 3.2, 3.3 | ✅ |
| `Robot.drive_wheels()` | `robi/robot.py` | 2.1, 2.2, 3 | ✅ |
| `calculate_center_distance()` | `robi/differential_drive.py` | 4.4 | ✅ |
| Encoder conversion helper (name TBD) | To decide | 4.1–4.3 | 🧪 |
| Odometry heading helper (name TBD) | To decide | 4.5 | 🧪 |
| Odometry pose estimator (name TBD) | To decide | 4.6, 4.7 | 🧪 |

---

## 💻 View Beautiful Math in VS Code

**Step 1:** Open `FORMULAS.md` in VS Code.

**Step 2:** Press **`Ctrl + Shift + V`** to open the Markdown preview.

**Step 3:** Or press **`Ctrl + K`**, then **`V`**, to open the preview beside the source.

> ✨ **Tip:** Text between `$$` lines becomes a nicely formatted equation in the preview. In Python comments, it stays plain text.

### 🧙‍♂️ Swaggy's rule

**Every time we add a new math function, update this book and the Python Function Map.** Keep Python docstrings short and clear, and keep the detailed formulas here.

---

*🤖 Built for Project ROBI — one small step at a time.*
