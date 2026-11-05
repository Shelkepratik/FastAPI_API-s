
import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ShopEase Dashboard",
    page_icon="🛒",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #f4f7fc;
    color: #17243d;
}

.block-container {
    padding-top: 1.5rem;
}

/* Main headings */
h1, h2, h3, h4 {
    color: #17243d !important;
}

/* General text */
.stApp p,
.stApp label,
.stApp [data-testid="stMarkdownContainer"] {
    color: #17243d;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #17243d;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #e5eaf3;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    color: #17243d !important;
}

/* Search and filter inputs */
.stTextInput input,
.stNumberInput input {
    background-color: white !important;
    color: #17243d !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: white !important;
    color: #17243d !important;
}

/* Product cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: white;
    border-radius: 14px;
    border: 1px solid #e5eaf3;
}

/* Product details */
.product-name {
    font-size: 19px;
    font-weight: bold;
    color: #17243d;
}

.product-price {
    font-size: 23px;
    font-weight: bold;
    color: #2563eb;
}

.stock {
    color: #16a34a !important;
    font-weight: bold;
}

.out-stock {
    color: #dc2626 !important;
    font-weight: bold;
}

/* Buttons */
.stButton button {
    background-color: #2563eb;
    color: white !important;
    border-radius: 8px;
    border: none;
}

.stButton button:hover {
    background-color: #1d4ed8;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------- API CONNECTION ----------------
def load_products():
    try:
        response = requests.get(
            f"{API_URL}/products",
            timeout=5
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException:
        st.error(
            "Cannot connect to FastAPI backend. "
            "Please start your API server."
        )
        return {}


# ---------------- SIDEBAR ----------------
st.sidebar.title("🛒 ShopEase")
st.sidebar.caption("E-Commerce Management")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Products", "About"]
)

st.sidebar.markdown("---")
st.sidebar.info("Smart Shopping, Better Living")


# ---------------- HEADER ----------------
st.title("👋 Welcome to ShopEase")
st.write("Discover the best products at great prices!")

products = load_products()


# ---------------- DASHBOARD PAGE ----------------
if page == "Dashboard":

    product_list = list(products.values())

    total_products = len(product_list)

    in_stock = sum(
        1 for product in product_list
        if product["stock"] > 0
    )

    average_rating = (
        sum(product["rating"] for product in product_list)
        / total_products
        if total_products > 0 else 0
    )

    inventory_value = sum(
        product["price"] * product["stock"]
        for product in product_list
    )

    # Dashboard statistics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📦 Total Products", total_products)
    col2.metric("🛒 In Stock", in_stock)
    col3.metric("⭐ Average Rating", f"{average_rating:.1f}")
    col4.metric("💰 Inventory Value", f"₹{inventory_value:,.0f}")

    st.markdown("---")

    # Search and filters
    st.subheader("🔎 Search and Filter Products")

    col1, col2, col3 = st.columns(3)

    with col1:
        search = st.text_input(
            "Search by name",
            placeholder="Enter product name..."
        )

    with col2:
        categories = ["All"]

        if product_list:
            categories += sorted(
                set(
                    product["category"]
                    for product in product_list
                )
            )

        category = st.selectbox(
            "Category",
            categories
        )

    with col3:
        max_price = st.number_input(
            "Maximum Price (₹)",
            min_value=0,
            value=100000
        )

    # Filter products
    filtered_products = {}

    for product_id, product in products.items():

        if search.lower() not in product["name"].lower():
            continue

        if (
            category != "All"
            and product["category"] != category
        ):
            continue

        if product["price"] > max_price:
            continue

        filtered_products[product_id] = product

    st.markdown("---")

    st.subheader("🛍️ Our Products")

    st.caption(
        f"Showing {len(filtered_products)} products"
    )

    if not filtered_products:
        st.warning("No products found.")

    else:
        product_items = list(filtered_products.items())

        # Display 3 products per row
        for i in range(0, len(product_items), 3):

            columns = st.columns(3)

            for column, item in zip(
                columns,
                product_items[i:i + 3]
            ):

                product_id, product = item

                with column:

                    with st.container(border=True):

                        st.markdown(
                            f"<div class='product-name'>"
                            f"{product['name']}</div>",
                            unsafe_allow_html=True
                        )

                        st.caption(
                            f"Product ID: {product_id}"
                        )

                        st.markdown(
                            f"**Category:** {product['category']}"
                        )

                        st.markdown(
                            f"**Brand:** {product['brand']}"
                        )

                        st.markdown(
                            f"<div class='product-price'>"
                            f"₹{product['price']:,}</div>",
                            unsafe_allow_html=True
                        )

                        if product["stock"] > 0:

                            st.markdown(
                                f"<span class='stock'>"
                                f"● In Stock ({product['stock']})"
                                f"</span>",
                                unsafe_allow_html=True
                            )

                        else:

                            st.markdown(
                                "<span class='out-stock'>"
                                "● Out of Stock"
                                "</span>",
                                unsafe_allow_html=True
                            )

                        st.write(
                            f"⭐ {product['rating']} / 5"
                        )

                        with st.expander("View Details"):
                            st.json(product)


# ---------------- PRODUCTS PAGE ----------------
elif page == "Products":

    st.subheader("📦 Product Catalog")

    if products:

        st.dataframe(
            [
                {
                    "Product ID": product_id,
                    **product
                }
                for product_id, product in products.items()
            ],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No products available.")


# ---------------- ABOUT PAGE ----------------
elif page == "About":

    st.subheader("ℹ️ About ShopEase")

    st.write("""
    ShopEase is an E-Commerce Product Management Dashboard.

    **Technologies Used:**
    - Python
    - Streamlit
    - FastAPI
    - JSON file for product storage

    **Features:**
    - View all products
    - Search products
    - Filter by category
    - Filter by maximum price
    - Check product stock
    - View product details
    """)
